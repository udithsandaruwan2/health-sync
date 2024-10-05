from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    path('', views.index, name='index'),    
    path('dashboard/', views.userDashboard, name='dashboard'),
    path('doctor/portal/', views.doctorDashboard, name='doctor-dashboard'),
    
    path('doctor/appointment/<str:pk>/', views.singleAppointment, name='appointment'),
    path('appointments/', views.userAppointments, name='user-appointments'),
    path('delete-appointment/<str:pk>/', views.deleteAppointment, name='delete-appointment'),
    
    path('requested-appointment/', views.requestedAppointment, name='requested-appointment'),
    
    path('profile/<str:pk>/', views.singleProfile, name='profile'),
    path('update-profile/', views.updateProfile, name='update-profile'),
    
]