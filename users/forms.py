from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import Profile, Appointment


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name', 
        }   
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'eg : Udith Sandaruwan', 'type':'text'},
        )

        self.fields['email'].widget.attrs.update(
            {'placeholder':'eg : udith@eventarc.com', 'type':'email'}
        )

        self.fields['username'].widget.attrs.update(
            {'placeholder': 'eg : udith002', 'type':'text'}
        )

        self.fields['password1'].widget.attrs.update(
            {'placeholder': '*************', 'type':'password'}
        )

        self.fields['password2'].widget.attrs.update(
            {'placeholder': '*************', 'type':'password'}
        )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image']


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'description']
