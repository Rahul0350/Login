from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
import applogin
from login import settings

#Nik
# Create your views here.


def home(request):
    # return render(request, "index.html")
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        FirstName = request.POST['FirstName']
        LastName = request.POST.get('LastName')
        Email = request.POST.get('Email')
        Password = request.POST['Password']
        Password2 = request.POST['Password2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists!please try some other')
            return redirect('home')
        if User.objects.filter(email=Email):
            messages.error(request, 'Email already exists!')
            return redirect('home')
        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
        if Password != Password2:
            messages.error(request, 'Password did not match')
        if not username.isalnum():
            messages.error(request, 'Username must be alphanumeric')
            return redirect('home')

        myuser = User.objects.create_user(username, Email, Password)
        myuser.first_name = FirstName
        myuser.last_name = LastName

        myuser.save()

        messages.success(request, 'Your account got created successfully')

        # Welcome Email

        # subject = "Welcome to omnywise!!"
        # message = "Hello " + myuser.first_name + "!!\n" + "Welcome to omnywise \n please confirm you email address \n Thank You"
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        Password = request.POST['Password']

        user = authenticate(username=username, password=Password)

        if user is not None:
            login(request, user)
            Firstname = user.first_name
            return render(request, "index.html", {"Firstname": Firstname})
        else:
            messages.error(request, "bad credentials")
            return redirect('home')

    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "logged out successfully!")
    return redirect('home')
