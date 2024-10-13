from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date

class Profile(models.Model):
    TYPES = [
        (1, 'Patient'),
        (2, 'Doctor')
    ]
    user_type = models.IntegerField(choices=TYPES, default=1)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    language = models.CharField(max_length=100, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, default='profiles/user-default.png', upload_to='profiles/')
    specialization = models.CharField(max_length=300, null=True, blank=True)  # Only for doctors
    medical_history = models.TextField(null=True, blank=True)  # Only for patients
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

class Appointment(models.Model):
    STATUS = (
        (1, 'Pending'),
        (2, 'Approved'),
        (3, 'Cancelled'),
        (4, 'Reviewed'),
    )
    
    patient = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 1},  # Only patients
        related_name='patient_appointments'  # Specify unique related_name
    )
    doctor = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 2},  # Only doctors
        related_name='doctor_appointments'  # Specify unique related_name
    )
    status = models.IntegerField(choices=STATUS, default=1)
    description = models.TextField(null=True, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(f"{self.doctor} : {self.patient}")


class LoyaltyPoint(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='loyalty_points')
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} - {self.points} points"