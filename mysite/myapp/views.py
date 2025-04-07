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



def custom_error(request, ):
    return render(request, 'error.html')


def login(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["u_name"]
            password = form.cleaned_data["u_password"]
            authenticated_user = authenticate(request, username=username, password=password)

            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                messages.success(request, f"Welcome, {username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {"form": form})