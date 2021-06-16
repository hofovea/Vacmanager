from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('upd_patient', views.update_patient, name='update_patient'),
    path('search_upd_patient', views.update_search_patient, name='update_search_patient'),
    path('add_vaccine_patient', views.add_vaccine_patient, name='add_vaccine_patient'),
    path('personal_vaccinations', views.personal_vaccinations, name='personal_vaccinations'),
    path('patient_queue', views.patient_queue, name='patient_queue'),
    path('doctor_queue', views.doctor_queue, name='doctor_queue'),
    path('upd_email', views.email_update, name='email_update'),
    path('upd_pass', views.password_update, name='password_update')
]
