from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from users.models import CustomUser


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


def email_update(request):
    if request.method == 'POST':
        print(request.user.email)
        user_to_upd = CustomUser.objects.get(email=request.user.email)
        user_to_upd.email = request.POST['email']
        user_to_upd.save()
        return redirect('/')


def password_update(request):
    if request.method == 'POST':
        password = request.POST['pass']
        user = request.user
        re_password = request.POST['re_pass']
        if password == re_password:
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('/')
