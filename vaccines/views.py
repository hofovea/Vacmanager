from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.datetime_safe import date
import dateutil.parser

from .models import *


# Create your views here.

def home(request):
    return render(request, 'home.html')


def get_life_period(age_in_years, age_in_months):
    if age_in_months <= 18:
        return LifePeriod.LifePeriods.BABY
    elif age_in_months > 18 and age_in_years <= 16:
        return LifePeriod.LifePeriods.CHILD
    else:
        return LifePeriod.LifePeriods.ADULT


def get_age_period(age_in_years, age_in_months, age_in_days):
    if age_in_days <= 1:
        return AgePeriod.AgePeriods.ONE_DAY
    elif 1 < age_in_days <= 5:
        return AgePeriod.AgePeriods.THREE_TO_FIVE_DAYS
    elif 2 <= age_in_months <= 3:
        return AgePeriod.AgePeriods.TWO_MONTHS
    elif 4 <= age_in_months <= 5:
        return AgePeriod.AgePeriods.FOUR_MONTHS
    elif 6 <= age_in_months <= 11:
        return AgePeriod.AgePeriods.SIX_MONTHS
    elif 12 <= age_in_months <= 17:
        return AgePeriod.AgePeriods.TWELVE_MONTHS
    elif age_in_months >= 18 and age_in_years <= 5:
        return AgePeriod.AgePeriods.EIGHTEEN_MONTHS
    elif 6 <= age_in_years <= 13:
        return AgePeriod.AgePeriods.SIX_YEARS
    elif 14 <= age_in_years <= 15:
        return AgePeriod.AgePeriods.FOURTEEN_YEARS
    elif age_in_years == 16:
        return AgePeriod.AgePeriods.SIXTEEN_YEARS
    else:
        return AgePeriod.AgePeriods.ADULT


def add_patient(request):
    if request.method == 'POST':
        print('add')
        patient_first_name = request.POST['patient_first_name']
        patient_last_name = request.POST['patient_first_name']
        patient_birthday = dateutil.parser.parse(request.POST['patient_birthday']).date()
        address_house_number = request.POST['address_house_number']
        address_street = request.POST['address_street']
        address_town = request.POST['address_town']

        # data-based calculations
        # calculate age in different formats
        today = date.today()
        patient_age_in_years = today.year - patient_birthday.year - (
                (today.month, today.day) < (patient_birthday.month, patient_birthday.day))
        print(patient_age_in_years)

        patient_age_in_months = (today.year - patient_birthday.year) * 12 + today.month - patient_birthday.month
        print(patient_age_in_months)

        patient_age_in_days = (today - patient_birthday).days
        print(patient_age_in_days)

        # get age_period and life_period entities
        patient_life_period = LifePeriod.objects.get(
            life_period=get_life_period(patient_age_in_years, patient_age_in_months))
        patient_age_period = AgePeriod.objects.get(
            age_period=get_age_period(patient_age_in_years, patient_age_in_months, patient_age_in_days))

        # new address creation
        new_address = Address(house=address_house_number, street=address_street, town=address_town)
        new_address.save()

        # new patient creation
        new_patient = Patient(name=patient_first_name, surname=patient_last_name, birthday=patient_birthday,
                              address=new_address, age=patient_age_in_years,
                              life_period=patient_life_period, age_period=patient_age_period)
        new_patient.save()
        return redirect('/')
    else:
        return render(request, 'add_patient.html')


def update_patient(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'upd_patient.html')


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
        if CustomUser.objects.filter(email=request.user.email).exists():
            print('Email taken')
            return HttpResponse('Email is taken')
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
