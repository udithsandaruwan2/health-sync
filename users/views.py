from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, AppointmentForm
from django.conf import settings
import requests
import os
from dotenv import load_dotenv
from .forms import ProfileForm
from .models import Profile, Appointment, LoyaltyPoint
from .utils import encrypt_message, decrypt_message
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .utils import send_email, auth_with_email
import logging
from django.utils.timezone import now

load_dotenv()
# Get the logger
logger = logging.getLogger('django')

def login_view(request):
    page = 'login'
    site_key = os.getenv('RECAPTCHA_PUBLIC_KEY')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        # Verify reCAPTCHA
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result.get('success'):
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Authenticate with email (OTP) - example function
                auth_call = auth_with_email(user)
                auth_code = auth_call['encrypted_otp']
                auth_message = auth_call['message']

                if auth_message == '200':
                    messages.success(request, 'User logged in successfully! OTP sent to your email.')

                    # Store encrypted OTP and user ID in session (server-side)
                    request.session['auth_code'] = auth_code
                    request.session['user_id'] = user.id

                    # Redirect to OTP verification page (no need for URL parameters)
                    return redirect('otp-verification')

                else:
                    messages.error(request, 'An error occurred during login!')
            else:
                messages.error(request, 'Username or password is incorrect!')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    context = {'page': page, 'site_key': site_key}
    return render(request, 'users/login-register.html', context)

def otp_verification(request):
    page = 'otp-verification'

    try:
        user_id = request.session.get('user_id')
        auth_code = request.session.get('auth_code')
        str_otp = decrypt_message(auth_code)

        # Fetch the user by ID
        user = get_object_or_404(User, id=user_id)

    except Exception as e:
        messages.error(request, 'Invalid or corrupted data. Please try again.')
        return redirect('login')

    if request.method == 'POST':
        otp_entered = request.POST['otp'].strip()

        if otp_entered == str_otp:
            messages.success(request, 'OTP verified successfully!')
            
            # Example of sending email
            send_email('User Login', f'User {user.username} logged in successfully!', [user.email])
            
            

            # Redirect based on user type
            if user.profile.user_type == 1:
                return redirect('dashboard')
            elif user.profile.user_type == 2:
                return redirect('doctor-dashboard')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    context = {'page': page, 'user': user}
    return render(request, 'users/otp-verification.html', context)

def register_view(request):
    page = 'register'
    form = CustomUserCreationForm()
    site_key = os.getenv('RECAPTCHA_PUBLIC_KEY')
    
    try:

        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            recaptcha_response = request.POST.get('g-recaptcha-response')
            
            # Verify reCAPTCHA
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result.get('success'):
                if form.is_valid():
                    user = form.save(commit=False)
                    user.username = user.username.lower()
                    user.save()
                    messages.success(request, 'User account was created!')
                    login(request, user)
                    
                    # Authenticate with email (OTP) - example function
                    auth_call = auth_with_email(user)
                    auth_code = auth_call['encrypted_otp']
                    auth_message = auth_call['message']

                    if auth_message == '200':
                        messages.success(request, 'User logged in successfully! OTP sent to your email.')

                        # Store encrypted OTP and user ID in session (server-side)
                        request.session['auth_code'] = auth_code
                        request.session['user_id'] = user.id

                        # Redirect to OTP verification page (no need for URL parameters)
                        return redirect('otp-verification')
                else:
                    messages.error(request, 'An error occurred during registration!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    except Exception as e:
        logger.error(f"An error occurred during login: {str(e)}", exc_info=True)
    
    logger.info(f"Processing login request...", extra={'user': request.user, 'request_path': request.path, 'time': now()})


    context = {'page': page, 'form': form, 'site_key': site_key}
    return render(request, 'users/login-register.html', context)

@login_required(login_url="login")
def logout_view(request):
    user = request.user
    try:
        logout(request)
        messages.info(request, 'User was logged out!')
        send_email('User Logout', f'User {user.username} logged out successfully!', [user.email])
        logger.info(f"User {user.username} logged out successfully.", extra={'user': user, 'request_path': request.path, 'time': now()})
    except Exception as e:
        logger.error(f"An error occurred during logout: {str(e)}", exc_info=True)
    return redirect('login')

def index(request):
    page = 'index'
    profile = None  # Use None instead of 'none'
    
    if request.user.is_authenticated:
        profile = request.user.profile
    
    logger.info(f"Rendering index page...", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    
    context = {'page': page, 'profile': profile}
    return render(request, 'users/index.html', context)


@login_required(login_url="login")
def userDashboard(request):
    page = 'user-dashboard'
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')
    page_encrypted = encrypt_message(page)
    
    appointments = Appointment.objects.all().filter(patient=profile, status=1)
    
    points, created = LoyaltyPoint.objects.get_or_create(user=profile)
    
    logger.info(f"Rendering user dashboard...", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    
    context = {'page': page, 'profile': profile, 'points': points, 'appointments': appointments, 'page_encrypted': page_encrypted}
    return render(request, 'users/user-dashboard.html', context)


def singleAppointment(request, pk):
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')
    
    doctor = Profile.objects.get(id=pk)
    form = AppointmentForm()
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = profile
            appointment.doctor = doctor
            appointment.save()
            messages.success(request, 'Appointment was created!')
            logger.info(f"Appointment created for patient {profile.user.username} with doctor {profile.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
            return redirect('appointment', pk=pk)
        else:
            logger.error(f"Appointment form is invalid for patient {profile.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    
    context = {'profile': profile, 'doctor': doctor, 'form': form}
    logger.info(f"Rendering single appointment page for doctor {profile.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    return render(request, 'users/single-appointment.html', context)

@login_required(login_url='login')
def updateProfile(request):
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')
    
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            logger.info(f"Profile for user {profile.user.username} updated successfully.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
            return redirect('update-profile')
        else:
            logger.error(f"Profile form is invalid for user {profile.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})

    context = {'form': form, 'profile': profile}
    logger.info(f"Rendering update profile page for user {profile.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    return render(request, 'users/update-profile.html', context)

@login_required(login_url='login')
def deleteAppointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    page_from = request.GET.get('page')
    page = decrypt_message(page_from)
    
    if request.method == 'POST':
        # Change status to 3 (assuming it means deleted/cancelled)
        appointment.status = 3
        appointment.save()  # Make sure to save the status change
        logger.info(f"Appointment {appointment.id} status changed to deleted by user {request.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
        # Redirect based on the page context
        if page == 'user-dashboard':
            return redirect('dashboard')
        else:
            return redirect('requested-appointment')
    
    context = {'appointment': appointment, 'page': page}
    logger.info(f"Rendering delete appointment page for appointment {appointment.id}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    return render(request, 'users/delete-appointment.html', context)

@login_required(login_url='login')
def doctorDashboard(request):
    page = 'doctor-dashboard'
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')

    appointments = Appointment.objects.all().filter(doctor=profile, status=2)
    
    logger.info(f"Rendering doctor dashboard for user {profile.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    
    context = {'page': page, 'profile': profile, 'appointments': appointments}
    return render(request, 'users/doctor-dashboard.html', context)

@login_required(login_url='login')
def requestedAppointment(request):
    page = 'request-appointment'
    page_encrypted = encrypt_message(page)
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')
    
    appointments = Appointment.objects.all().filter(doctor=profile, status=1)
    
    logger.info(f"Rendering requested appointments page for doctor {profile.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    
    context = {'page': page, 'appointments': appointments, 'page_encrypted': page_encrypted}
    return render(request, 'users/requested-appointments.html', context)

@login_required(login_url='login')
def approveAppointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    page = 'approve-appointment'
    
    if request.method == 'POST':
        appointment.status = 2
        appointment.save()
        messages.success(request, 'Appointment was approved!')
        logger.info(f"Appointment {appointment.id} approved by user {request.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
        return redirect('requested-appointment')
    
    context = {'page': page, 'appointment': appointment}
    logger.info(f"Rendering approve appointment page for appointment {appointment.id}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    return render(request, 'users/approve-appointment.html', context)

def singleProfileView(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
        logger.info(f"Rendering single profile view for profile {profile.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    except Profile.DoesNotExist:
        logger.error(f"Profile with id {pk} does not exist.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
        messages.error(request, 'Profile not found.')
        return redirect('index')

    context = {'profile': profile}
    return render(request, 'users/single-profile-view.html', context)

def doctors(request):
    page = 'doctors'
    profile = None  # Use None instead of 'none'
    
    if request.user.is_authenticated:
        profile = request.user.profile
    doctors = Profile.objects.all().filter(user_type=2)
    logger.info(f"Rendering doctors page.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    context = {'page': page, 'doctors': doctors, 'profile': profile}
    return render(request, 'users/doctors.html', context)

def about(request):
    page = 'about'
    profile = None  # Use None instead of 'none'
        
    if request.user.is_authenticated:
        profile = request.user.profile
    logger.info(f"Rendering about page.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    context = {'page': page, 'profile': profile}
    return render(request, 'users/about.html', context)

def contactUs(request):
    page = 'contact-us'
    profile = None  # Use None instead of 'none'
        
    if request.user.is_authenticated:
        profile = request.user.profile
    logger.info(f"Rendering contact us page.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
    context = {'page': page, 'profile': profile}
    return render(request, 'users/contact-us.html', context)

@login_required(login_url='login')
def reviewedAppointment(request, pk):
    page = 'reviewed-appointment'
    profile = None  # Use None instead of 'none'
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')
    
    appointment = get_object_or_404(Appointment, id=pk)
    
    if request.method == 'POST':
        appointment.status = 4
        appointment.save()
        messages.success(request, 'Appointment was marked as reviewed!')
        logger.info(f"Appointment {appointment.id} marked as reviewed by user {request.user.username}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})
        return redirect('doctor-dashboard')
    
    context = {'page': page}
    logger.info(f"Rendering reviewed appointment page for appointment {appointment.id}.", extra={'user': request.user, 'request_path': request.path, 'time': now()})