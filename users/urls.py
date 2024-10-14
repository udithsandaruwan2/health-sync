from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    path('otp-verification/', views.otp_verification, name='otp-verification'),
    
    path('', views.index, name='index'),    
    path('dashboard/', views.userDashboard, name='dashboard'),
    path('doctor/portal/', views.doctorDashboard, name='doctor-dashboard'),
    
    path('doctor/appointment/<str:pk>/', views.singleAppointment, name='appointment'),
    path('delete-appointment/<str:pk>/', views.deleteAppointment, name='delete-appointment'),
    
    path('requested-appointment/', views.requestedAppointment, name='requested-appointment'),
    path('approve-appointment/<str:pk>/', views.approveAppointment, name='approve-appointment'),
    

    path('profile-view/<str:pk>/', views.singleProfileView, name='view-profile'),
    path('update-profile/', views.updateProfile, name='update-profile'),
    
    path('doctors/', views.doctors, name='doctors'),
    path('about/', views.about, name='about'),
    path('contact-us/', views.contactUs, name='contact-us')
    
    
    
]