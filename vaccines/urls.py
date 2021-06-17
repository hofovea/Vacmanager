from django.contrib import admin
from django.urls import path
from . import views
from .table_views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('upd_patient', views.update_patient, name='update_patient'),
    path('search_upd_patient', views.search_update_patient, name='update_search_patient'),

    path('add_vaccination', views.add_vaccination, name='add_vaccination'),
    path('search_add_vaccination', views.search_add_vaccination, name='search_add_vaccination'),
    path('upd_vaccination', views.update_vaccination, name='update_vaccination'),
    path('search_patient_vaccination', views.search_patient_vaccination, name='search_patient_vaccination'),
    path('search_upd_vaccination', views.search_update_vaccination, name='search_update_vaccination'),

    #path('vaccination_results', views.vaccination_results, name='vaccination_results'),
    path('vaccination_results', PatientListView.as_view(), name='vaccination_results'),
    path('patient_results', VaccinationListView.as_view(), name='patient_results'),

    path('queue', views.queue, name='doctor_queue'),
    path('add_queue', views.add_queue, name='doctor_queue'),

    path('upd_email', views.email_update, name='email_update'),
    path('upd_pass', views.password_update, name='password_update'),

    # patient`s personal vaccination
    path('personal_vaccinations', views.personal_vaccinations, name='personal_vaccinations'),

    # analysis
    path('circle', views.circle, name='circle'),
    path('histogram', views.histogram, name='histogram')
]
