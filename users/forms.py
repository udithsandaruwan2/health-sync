from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import Profile, Appointment, LoyaltyPoint


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']
        labels = {
            'first_name':'Name', 
        }   
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update(
            {'type':'text', 'class':"form-control"}
        )

        self.fields['email'].widget.attrs.update(
            {'type':'email', 'class':"form-control"}
        )

        self.fields['password1'].widget.attrs.update(
            {'type':'password', 'class':"form-control"}
        )

        self.fields['password2'].widget.attrs.update(
            {'type':'password', 'class':"form-control"}
        )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image', 'date_of_birth', 'gender', 'language']
        
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {'class':"form-control"}
        )

        self.fields['email'].widget.attrs.update(
            {'class':"form-control"}
        )

        self.fields['username'].widget.attrs.update(
            {'class':"form-control"}
        )

        self.fields['location'].widget.attrs.update(
            {'class':"form-control"}
        )

        self.fields['short_intro'].widget.attrs.update(
            {'class':"form-control"}
        )

        self.fields['bio'].widget.attrs.update(
            {'class':"form-control"}
        )

        self.fields['profile_image'].widget.attrs.update(
            {'class':"form-control"}
        )

        self.fields['date_of_birth'].widget.attrs.update(
            {'class':"form-control", 'type': 'date', 'id': 'dob'}
        )

        self.fields['gender'].widget.attrs.update(
            {'class':"form-control"}
        )

        self.fields['language'].widget.attrs.update(
            {'class':"form-control"}
        )


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'description']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
        def __init__(self, *args, **kwargs):
            super(AppointmentForm, self).__init__(*args, **kwargs)

            self.fields['appointment_date'].widget.attrs.update(
                {'class':"form-control"}
            )

            self.fields['appointment_time'].widget.attrs.update(
                {'class':"form-control"}
            )

            self.fields['description'].widget.attrs.update(
                {'class':"form-control"}
            )