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


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(request, username=user.username, password=form.cleaned_data["u_password"])

            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                messages.success(request, "Your account has been successfully created.")
                return redirect("home")
            else:
                messages.error(request, "User registration failed. Please try again.")
        else:
            messages.error(request, "Invalid form data. Please check your inputs.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_form = UserProfileForm(instance=user_profile)
    user_form = UserForm(instance=request.user)
    general_appointments = GeneralAppointment.objects.filter(user=request.user)
    chapter_appointments = ChapterAppointment.objects.filter(user=request.user)

    if request.method == "POST":
        if "delete_account" in request.POST:
            request.user.delete()
            auth_logout(request)
            messages.success(request, "Your account has been deleted.")
            return redirect('login')

        profile_form = UserProfileForm(request.POST, instance=user_profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')
        else:
            messages.error(request, "Error updating profile. Please check the form.")

    context = {
        'user_profile': user_profile,
        'profile_form': profile_form,
        'user_form': user_form,
        'general_appointments': general_appointments,
        'chapter_appointments': chapter_appointments,
    }
    return render(request, 'user_profile.html', context)


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('home')

def tutor_list_general(request):
    specialty = request.GET.get('specialty')
    gender = request.GET.get('gender')
    medium = request.GET.get('medium')
    division = request.GET.get('division')
    district = request.GET.get('district')
    background = request.GET.get('background')

    generaltutor = GeneralTutor.objects.all()
    if specialty:
        generaltutor = generaltutor.filter(specialty__icontains=specialty)
    if gender:
        generaltutor = generaltutor.filter(gender__iexact=gender)
    if medium:
        generaltutor = generaltutor.filter(medium__icontains=medium)
    if division:
        generaltutor = generaltutor.filter(division__icontains=division)
    if district:
        generaltutor = generaltutor.filter(district__icontains=district)
    if background:
        generaltutor = generaltutor.filter(background__icontains=background)


    return render(request, 'tutor_list_general.html', {
        'generaltutor': generaltutor,
        'specialty': dict(GeneralTutor.SPECIALTY_CHOICES).get(specialty, 'All'),
    })