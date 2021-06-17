from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.sign_in, name='login'),
    path('registration', views.register, name='register'),
    path('logout', views.sign_out, name='logout'),
    path('link_user', views.link_with_patient, name='link_user'),
    path('user_patient_creation', views.user_patient_creation, name='user_patient_creation'),
]
