from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.sign_in, name='login'),
    path('registration', views.register, name='register'),
    path('logout', views.sign_out, name='register'),
]
