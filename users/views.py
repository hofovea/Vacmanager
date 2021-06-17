from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from users.models import CustomUser
from vaccines.models import Patient, LifePeriod, AgePeriod, Address
from vaccines.views import get_birthday_in_years, get_birthday_in_months, get_birthday_in_days, get_life_period, \
    get_age_period
import dateutil.parser


def sign_in(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            print('already signed in')
            return redirect('/')
        email = request.POST['email']
        password = request.POST['pass']
        # if 'is_remember' in request.POST:
        #     is_remember = request.POST['is_remember']
        user = auth.authenticate(username=email, password=password)
        print(request.user.is_authenticated)
        if user is not None:
            login(request, user)
            return redirect('/')
        return HttpResponse('no such user')

    else:
        return render(request, 'user/login.html')


@login_required(login_url='login')
def sign_out(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('login')
        return redirect('/')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        last_name = request.POST['surname']
        email = request.POST['email']
        password = request.POST['pass']
        re_password = request.POST['re_pass']
        if password == re_password:
            if CustomUser.objects.filter(email=email).exists():
                print('User already exists')
                return HttpResponse('User already exists')
            else:
                user = CustomUser.objects.create_user(email, password)
                user.last_name = last_name
                user.first_name = first_name
                user.save()
                print('new user added')
                user = auth.authenticate(username=email, password=password)
                print(request.user.is_authenticated)
                login(request, user)
                return redirect('link_user')
        else:
            return HttpResponse('Passwords do not match')
    else:
        return render(request, 'user/register.html')


def link_with_patient(request):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, email=request.user.email)
        patient_first_name = user.first_name
        patient_last_name = user.last_name
        patient_birthday = request.POST['patient_birthday']
        try:
            patient = Patient.objects.get(name=patient_first_name, surname=patient_last_name, birthday=patient_birthday)
        except Patient.DoesNotExist:
            patient = None
        if patient is None:
            return redirect('user_patient_creation')
        else:
            user.patient = patient
            user.save()
            return redirect('/')
    else:
        return render(request, 'patient/patient_search.html',
                      {'action_name': 'Зв\'язування з пацієнтом', 'action_url': 'link_user'})


def user_patient_creation(request):
    user = get_object_or_404(CustomUser, email=request.user.email)
    if request.method == 'POST':
        print('add')
        patient_first_name = request.POST['patient_first_name']
        patient_last_name = request.POST['patient_last_name']
        patient_birthday = dateutil.parser.parse(request.POST['patient_birthday']).date()
        address_house_number = request.POST['address_house_number']
        address_street = request.POST['address_street']
        address_town = request.POST['address_town']

        # data-based calculations
        # calculate age in different formats
        patient_age_in_years = get_birthday_in_years(patient_birthday)
        print(patient_age_in_years)

        patient_age_in_months = get_birthday_in_months(patient_birthday)
        print(patient_age_in_months)

        patient_age_in_days = get_birthday_in_days(patient_birthday)
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
        new_patient.user = user
        new_patient.save()
        return redirect('/')
    else:
        return render(request, 'user/user_patient_creation.html', {'user': user})
