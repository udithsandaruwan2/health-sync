from django.db import models
from django.contrib.auth.models import User
import uuid

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
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, default='profiles/user-default.png', upload_to='profiles/')
    specialization = models.CharField(max_length=300, null=True, blank=True)  # Only for doctors
    medical_history = models.TextField(null=True, blank=True)  # Only for patients
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

class Appointment(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
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
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.doctor} : {self.patient}"
