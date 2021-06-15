from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctor', views.home_doctor, name='home_doctor'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('add_vaccine_patient', views.add_vaccine_patient, name='add_vaccine_patient'),
    path('personal_vaccinations', views.personal_vaccinations, name='personal_vaccinations'),
    path('patient_queue', views.patient_queue, name='patient_queue'),
    path('doctor_queue', views.doctor_queue, name='doctor_queue'),
]
