import json
from collections import Counter
from django.db.models import F
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.datetime_safe import date
import dateutil.parser
import pandas as pd
from plotly.graph_objs import Scatter
from plotly.offline import plot
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from .models import *

# Create your views here.
from .tables import *


def home(request):
    return render(request, 'index.html')


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


def get_birthday_in_years(birthday):
    today = date.today()
    return today.year - birthday.year - (
            (today.month, today.day) < (birthday.month, birthday.day))


def get_birthday_in_months(birthday):
    today = date.today()
    return (today.year - birthday.year) * 12 + today.month - birthday.month


def get_birthday_in_days(birthday):
    today = date.today()
    return (today - birthday).days


def add_patient(request):
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
        new_patient.save()
        return redirect('/')
    else:
        return render(request, 'patient/patient_add.html')


def search_update_patient(request):
    if request.method == 'POST':
        patients = Patient.objects.all()
        patient_first_name = request.POST['patient_first_name']
        patient_last_name = request.POST['patient_last_name']
        patient_birthday = dateutil.parser.parse(request.POST['patient_birthday']).date()
        try:
            patient = Patient.objects.get(name=patient_first_name, surname=patient_last_name, birthday=patient_birthday)
        except Patient.DoesNotExist:
            patient = None
        if patient is None:
            return render(request, 'patient/patient_search.html',
                          {'patient_not_found': '???????????????? ?? ???????????? ???????????? ???? ??????????',
                           'action_name': '?????????????????????? ????????????????', 'action_url': 'search_upd_patient',
                           'patients': patients})
        else:
            return render(request, 'patient/patient_update.html',
                          {'patient_to_update': patient})
    else:
        patients = Patient.objects.all()
        return render(request, 'patient/patient_search.html',
                      {'action_name': '?????????????????????? ????????????????', 'action_url': 'search_upd_patient', 'patients': patients})


def update_patient(request):
    if request.method == 'POST':
        print('update')
        patient_first_name = request.POST['patient_first_name']
        patient_last_name = request.POST['patient_last_name']
        patient_birthday = dateutil.parser.parse(request.POST['patient_birthday']).date()
        address_house_number = request.POST['address_house_number']
        address_street = request.POST['address_street']
        address_town = request.POST['address_town']
        patient_id = request.POST['patient_id']

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

        patient_to_update = get_object_or_404(Patient, id=patient_id)
        patient_to_update_address = get_object_or_404(Address, id=patient_to_update.address.id)

        patient_to_update_address.house = address_house_number
        patient_to_update_address.street = address_street
        patient_to_update_address.town = address_town

        patient_to_update.name = patient_first_name
        patient_to_update.surname = patient_last_name
        patient_to_update.birthday = patient_birthday
        patient_to_update.age = patient_age_in_years
        patient_to_update.age_period = patient_age_period
        patient_to_update.life_period = patient_life_period

        patient_to_update_address.save()
        patient_to_update.save()
        return redirect('/')


def get_life_period_string(life_period):
    if life_period == 1:
        return '??????????????'
    elif life_period == 2:
        return '????????????'
    else:
        return '????????????????'


def get_age_period_string(age_period):
    if age_period == 1:
        return '1 ????????'
    elif age_period == 2:
        return '2-5 ????????'
    elif age_period == 3:
        return '2 ????????????'
    elif age_period == 4:
        return '4 ????????????'
    elif age_period == 5:
        return '6 ??????????????'
    elif age_period == 6:
        return '12 ??????????????'
    elif age_period == 7:
        return '18 ??????????????'
    elif age_period == 8:
        return '6 ??????????'
    elif age_period == 9:
        return '14 ??????????'
    elif age_period == 10:
        return '16 ??????????'
    else:
        return '????????????????'


def add_vaccination(request):
    if request.method == 'POST':
        number_of_dose = request.POST['number_of_dose']
        scheduled_vaccination_date = dateutil.parser.parse(request.POST['scheduled_vaccination_date']).date()
        actual_vaccination_date = dateutil.parser.parse(request.POST['actual_vaccination_date']).date()
        vaccine_id = request.POST['vaccine_id']
        patient_id = request.POST['patient_id']

        patient = get_object_or_404(Patient, id=patient_id)
        vaccine = get_object_or_404(Vaccine, id=vaccine_id)
        new_vaccination_date = VaccinationDate.objects.create(patient=patient, vaccine=vaccine,
                                                              number_of_dose=number_of_dose,
                                                              scheduled_date=scheduled_vaccination_date,
                                                              actual_date=actual_vaccination_date)
        new_vaccination_date.save()
        return redirect('/')


def search_add_vaccination(request):
    patients = Patient.objects.all()
    if request.method == 'POST':
        patient_first_name = request.POST['patient_first_name']
        patient_last_name = request.POST['patient_last_name']
        patient_birthday = dateutil.parser.parse(request.POST['patient_birthday']).date()
        try:
            patient = Patient.objects.get(name=patient_first_name, surname=patient_last_name, birthday=patient_birthday)
        except Patient.DoesNotExist:
            patient = None
        if patient is None:
            return render(request, 'patient/patient_search.html',
                          {'patient_not_found': '???????????????? ?? ???????????? ???????????? ???? ??????????',
                           'action_name': '?????????????????? ???????????????????? ?????? ???????????????? ????????????????',
                           'action_url': 'search_add_vaccination', 'patients': patients})
        else:
            all_vaccines = Vaccine.objects.all()
            return render(request, 'vaccination/vaccination_add.html',
                          {'patient': patient, 'age_period': get_age_period_string(patient.age_period.age_period),
                           'life_period': get_life_period_string(patient.life_period.life_period),
                           'vaccines': all_vaccines})
    else:
        return render(request, 'patient/patient_search.html',
                      {'action_name': '?????????????????? ???????????????????? ?????? ???????????????? ????????????????',
                       'action_url': 'search_add_vaccination', 'patients': patients})


def update_vaccination(request):
    if request.method == 'POST':
        number_of_dose = request.POST['number_of_dose']
        scheduled_vaccination_date = dateutil.parser.parse(request.POST['scheduled_vaccination_date']).date()
        actual_vaccination_date = dateutil.parser.parse(request.POST['actual_vaccination_date']).date()
        patient_id = request.POST['patient_id']
        vaccination_id = request.POST['vaccination_id']
        patient = get_object_or_404(Patient, id=patient_id)
        vaccination = get_object_or_404(VaccinationDate, id=vaccination_id)

        vaccination.scheduled_date = scheduled_vaccination_date
        vaccination.actual_date = actual_vaccination_date
        vaccination.number_of_dose = number_of_dose
        vaccination.save()
        return redirect('/')


def search_update_vaccination(request):
    patients = Patient.objects.all()
    if request.method == 'POST':
        patient_first_name = request.POST['patient_first_name']
        patient_last_name = request.POST['patient_last_name']
        patient_birthday = dateutil.parser.parse(request.POST['patient_birthday']).date()
        try:
            patient = Patient.objects.get(name=patient_first_name, surname=patient_last_name, birthday=patient_birthday)
        except Patient.DoesNotExist:
            patient = None
        if patient is None:
            return render(request, 'patient/patient_search.html',
                          {'patient_not_found': '???????????????? ?? ???????????? ???????????? ???? ??????????',
                           'action_name': '?????????????????????? ???????????????????? ?????? ???????????????? ????????????????',
                           'action_url': 'search_upd_vaccination', 'patients': patients})
        else:
            return render(request, 'vaccination/vaccination_search.html',
                          {'action_url': 'search_patient_vaccination', 'patient': patient,
                           'vaccinations': patient.vaccination_dates.all()})
    else:
        return render(request, 'patient/patient_search.html',
                      {'action_name': '?????????????????????? ???????????????????? ?????? ???????????????? ????????????????',
                       'action_url': 'search_upd_vaccination', 'patients': patients})


def search_patient_vaccination(request):
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        vaccination_id = request.POST['vaccination_id']
        patient = Patient.objects.get(id=patient_id)
        vaccination = VaccinationDate.objects.get(id=vaccination_id)
        return render(request, 'vaccination/vaccination_update.html',
                      {'patient': patient, 'age_period': get_age_period_string(patient.age_period.age_period),
                       'life_period': get_life_period_string(patient.life_period.life_period),
                       'vaccination': vaccination})
    else:
        return render(request, 'patient/patient_search.html',
                      {'action_name': '?????????????????????? ???????????????????? ?????? ???????????????? ????????????????',
                       'action_url': 'upd_vaccination'})


def personal_vaccinations(request):
    user = get_object_or_404(CustomUser, email=request.user.email)
    patient = get_object_or_404(Patient, id=user.patient.id)
    vaccinations = patient.vaccination_dates.all()
    return render(request, 'vaccination/vaccinations_personal.html', {'vaccinations': vaccinations})


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


def queue(request):
    user = get_object_or_404(CustomUser, email=request.user.email)
    if request.method == 'POST':
        if user.is_doctor:
            queue = get_object_or_404(Queue, id=request.POST['queue_id'])
            queue.is_active = not queue.is_active
            queue.save()
            return redirect('/queue')
        else:
            queue = get_object_or_404(Queue, id=request.POST['queue_id'])
            queue.patients.add(user.patient)
            queue.save()
            return redirect('/queue')
    else:
        if not user.is_doctor:
            queues = Queue.objects.all().order_by('date')
            patient = user.patient
            return render(request, 'queue/queue.html', {'queues': queues, 'patient_queues': patient.queues.all()})
        else:
            queues = Queue.objects.all().order_by('date')
            return render(request, 'queue/queue.html', {'queues': queues})


def add_queue(request):
    if request.method == 'POST':
        queue_date = request.POST['queue_date']
        new_queue = Queue.objects.create(date=queue_date, is_active=True)
        new_queue.save()
        return redirect('/queue')
    else:
        return render(request, 'queue/queue_add.html')


def circle(request):
    x_data = list(Patient.objects.all().values('age'))  # [0, 1, 2, 3]
    data_1 = len(list(VaccinationDate.objects.filter(scheduled_date=F('actual_date'))))
    data_2 = len(list(VaccinationDate.objects.all()))
    df = pd.DataFrame({'names': ['????????????', '????????????????'], 'data': [data_1, data_2]})
    # print(x_data)
    count = Counter()
    for x in x_data:
        count[str(x['age'])] += 1
    count_list = list(count.items())  # [{count[count.keys][count.values]: list()}]
    # print(count)
    # print(count.values())
    # df = pd.DataFrame({'count': count.values()})

    plot_h = px.pie(names=['????????????', '????????????????'], values=[data_1, data_2])

    #plot_h = px.pie(names=count.keys(), values=count.values())

    # plot_div = plot([Scatter(x=x_data, y=y_data,
    #                          mode='markers', name='test',
    #                          opacity=0.8, marker_color='green')],
    #                 output_type='div')
    # return HttpResponse(plot_h.to_html())
    return render(request, 'analysis/circle.html', context={'plot_div': plot_h.to_html()})


def histogram(request):
    x_data = list(Patient.objects.all().values('age'))  # [0, 1, 2, 3]
    print(x_data)
    count = Counter()
    for x in x_data:
        count[str(x['age'])] += 1
    count_list = list(count.items())  # [{count[count.keys][count.values]: list()}]
    print(count)
    print(count_list)
    df = pd.DataFrame({'count': dict(count)})
    plot_h = px.bar(df, )
    # plot_h = px.bar(x_data, y='age')
    return render(request, 'analysis/histogram.html', context={'plot_div': plot_h.to_html()})
