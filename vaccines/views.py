from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'home.html', {'log': 'Please login', 'reg': 'Please register'})


def home_doctor(request):
    return render(request, 'home_doctor.html', {'log': 'Please login', 'reg': 'Please register'})


def add_patient(request):
    return render(request, 'add_patient.html', {'log': 'Please login', 'reg': 'Please register'})


def add_vaccine_patient(request):
    return render(request, 'add_vaccine_patient.html', {'log': 'Please login', 'reg': 'Please register'})


def personal_vaccinations(request):
    return render(request, 'personal_vaccinations.html', {'log': 'Please login', 'reg': 'Please register'})


def patient_queue(request):
    return render(request, 'patient_queue.html', {'log': 'Please login', 'reg': 'Please register'})


def doctor_queue(request):
    return render(request, 'doctor_queue.html', {'log': 'Please login', 'reg': 'Please register'})
