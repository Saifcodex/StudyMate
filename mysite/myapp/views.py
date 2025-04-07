from django.shortcuts import render
from .models import *
from .forms import  UserProfileForm, UserForm  , RegisterForm , LoginForm
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')