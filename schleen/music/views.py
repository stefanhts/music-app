from django.shortcuts import render
from .models import User


def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')

def user(request):

    users = User.objects.all()


    return render(request, 'user.html', {'usrs':users})