from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                return redirect('register')
                messages.info(request, 'This email is already associated with an account')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, last_name=last_name,
                                                first_name=first_name)
                user.save()
                print('user created')
                return redirect('/')
        else:
            messages.info(request, 'Passwords do not match')
            print('passwords do not match')
            return redirect('register')

    else:
        return render(request, 'register.html')


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password =request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
           auth.login(request, user)
           return redirect('/')

        else:
            messages.info(request, 'invalid credentials')
            return redirect('/login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')