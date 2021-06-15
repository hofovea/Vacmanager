from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import login

# Create your views here.
from users.models import CustomUser


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
        return render(request, 'login.html')


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
                return redirect('/')
        else:
            return HttpResponse('Passwords do not match')
    else:
        return render(request, 'register.html')