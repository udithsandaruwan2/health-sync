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

load_dotenv()

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
                messages.success(request, 'User login successfully!')
                if user.profile.user_type == 1:
                    return redirect('dashboard')
                
                if user.profile.user_type == 2:
                    return redirect('doctor-dashboard')
            else:
                messages.error(request, 'Username or password is incorrect!')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    context = {'page': page, 'site_key': site_key}
    return render(request, 'users/login-register.html', context)

def register_view(request):
    page = 'register'
    form = CustomUserCreationForm()
    site_key = os.getenv('RECAPTCHA_PUBLIC_KEY')

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
                return redirect('dashboard')
            else:
                messages.error(request, 'An error occurred during registration!')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    context = {'page': page, 'form': form, 'site_key': site_key}
    return render(request, 'users/login-register.html', context)

@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

def index(request):
    page = 'index'
    doctores = Profile.objects.all().filter(user_type=2)
    context = {'page': page, 'doctores': doctores}
    return render(request, 'users/index.html', context)

@login_required(login_url="login")
def userDashboard(request):
    page = 'user-dashboard'
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')
    
    doctors = Profile.objects.all().filter(user_type=2)
    points, created = LoyaltyPoint.objects.get_or_create(user=profile)
    
    context = {'page': page, 'profile':profile, 'doctors': doctors, 'points': points}
    return render(request, 'users/user-dashboard.html', context)

@login_required(login_url="login")
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

            return redirect('appointment', pk=pk)
    
    context = {'profile': profile, 'doctor': doctor, 'form':form}
    return render(request, 'users/single-appointment.html', context)

@login_required(login_url="login")
def userAppointments(request):
    page = 'user-appointments'
    page_encrypted = encrypt_message(page)
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')
    appointments = Appointment.objects.all().filter(patient=profile)
    
    context = {'page':page, 'profile': profile, 'appointments': appointments, 'page_encrypted': page_encrypted}
    return render(request, 'users/user-appointments.html', context)

@login_required(login_url="login")
def singleProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    context = {'profile': profile}
    return render(request, 'users/single-profile.html', context)

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
            return redirect('profile', pk=profile.id)

    context = {'form': form}
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
        # Redirect based on the page context
        if page == 'user-appointments':
            return redirect('user-appointments')
        else:
            return redirect('requested-appointment')
    
    context = {'appointment': appointment, 'page': page}
    return render(request, 'users/delete-appointment.html', context)

@login_required(login_url='login')
def doctorDashboard(request):
    page = 'doctor-dashboard'
    profile = request.user.profile
    appointments = Appointment.objects.all().filter(doctor=profile, status=2)
    try:
        profile = request.user.profile
    except AttributeError:
        return redirect('login')

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
    context = {'page': page, 'appointments':appointments, 'page_encrypted': page_encrypted}
    return render(request, 'users/requested-appointments.html', context)

@login_required(login_url='login')
def approveAppointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    page = 'approve-appointment'
    
    if request.method == 'POST':
        appointment.status = 2
        appointment.save()
        messages.success(request, 'Appointment was approved!')
        return redirect('requested-appointment')
    
    context = {'page': page, 'appointment': appointment}
    return render(request, 'users/approve-appointment.html', context)

def singleProfileView(request, pk):
    profile = Profile.objects.get(id=pk)
    
    context = {'profile': profile}
    return render(request, 'users/single-profile-view.html', context)