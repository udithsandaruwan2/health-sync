from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.conf import settings
import requests
import os
from dotenv import load_dotenv
from .forms import ProfileForm
from .models import Profile

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
                return redirect('dashboard')
            else:
                messages.error(request, 'Username or password is incorrect!')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    context = {'page': page, 'site_key': site_key}
    return render(request, 'users/login-register.html', context)


def register_view(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'An error occurred during registration!')

    context = {'page': page, 'form': form}
    return render(request, 'users/login-register.html', context)

@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

def index(request):
    return render(request, 'users/index.html')

@login_required(login_url="login")
def dashboard(request):
    page = 'dashboard'
    profile = request.user.profile
    
    doctors = Profile.objects.all().filter(user_type=2)
    
    context = {'page': page, 'profile':profile, 'doctors': doctors}
    return render(request, 'users/dashboard.html', context)

@login_required(login_url="login")
def singleAppointment(request, pk):
    profile = request.user.profile

    doctor = Profile.objects.get(id=pk)
    
    context = {'profile': profile, 'doctor': doctor}
    return render(request, 'users/single-appointment.html', context)

def singleProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    context = {'profile': profile}
    return render(request, 'users/single-profile.html', context)

def updateProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=profile.id)

    context = {'form': form}
    return render(request, 'users/update-profile.html', context)
