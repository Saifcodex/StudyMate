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

def tutor_list_chapter(request):
    specialty = request.GET.get('specialty')
    gender = request.GET.get('gender')
    medium = request.GET.get('medium')
    division = request.GET.get('division')
    district = request.GET.get('district')
    background = request.GET.get('background')

    chaptertutor = ChapterTutor.objects.all()
    if specialty:
        chaptertutor = chaptertutor.filter(specialty__icontains=specialty)
    if gender:
        chaptertutor = chaptertutor.filter(gender__iexact=gender)
    if medium:
        chaptertutor = chaptertutor.filter(medium__icontains=medium)
    if division:
        chaptertutor = chaptertutor.filter(division__icontains=division)
    if district:
        chaptertutor = chaptertutor.filter(district__icontains=district)
    if background:
        chaptertutor = chaptertutor.filter(background__icontains=background)

    return render(request, 'tutor_list_chapter.html', {
        'chaptertutor': chaptertutor,
        'specialty': dict(ChapterTutor.SPECIALTY_CHOICES).get(specialty, 'All'),
    })

@login_required
def book_appointment_general(request, general_tutor_id):
    if request.method == "POST":
        generaltutor = get_object_or_404(GeneralTutor, id=general_tutor_id)
        student_name = request.POST.get('student_name')
        phone_number = request.POST.get('phone_number')
        guardian_name = request.POST.get('guardian_name')
        guardian_phone = request.POST.get('guardian_phone')
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        division = request.POST.get('division')
        district = request.POST.get('district')
        address = request.POST.get('address')
        preferred_days = request.POST.get('preferred_days')
        preferred_time = request.POST.get('preferred_time')

        GeneralAppointment.objects.create(
            user=request.user,
            generaltutor=generaltutor,
            student_name=student_name,
            phone_number=phone_number,
            guardian_name=guardian_name,
            guardian_phone=guardian_phone,
            class_name=class_name,
            subject=subject,
            division=division,
            district=district,
            address=address,
            preferred_days=preferred_days,
            preferred_time=preferred_time,
        )
        messages.success(request, "Appointment booked successfully.")
        return redirect('user_profile')

    return redirect('tutor_list_general')

@login_required
def book_appointment_chapter(request, chapter_tutor_id):
    if request.method == "POST":
        chaptertutor = get_object_or_404(ChapterTutor, id=chapter_tutor_id)
        student_name = request.POST.get('student_name')
        phone_number = request.POST.get('phone_number')
        guardian_name = request.POST.get('guardian_name')
        guardian_phone = request.POST.get('guardian_phone')
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        chapter = request.POST.get('chapter')
        division = request.POST.get('division')
        district = request.POST.get('district')
        address = request.POST.get('address')
        preferred_days = request.POST.get('preferred_days')
        preferred_time = request.POST.get('preferred_time')

        ChapterAppointment.objects.create(
            user=request.user,
            chaptertutor=chaptertutor,
            student_name=student_name,
            phone_number=phone_number,
            guardian_name=guardian_name,
            guardian_phone=guardian_phone,
            class_name=class_name,
            subject=subject,
            chapter=chapter,
            division=division,
            district=district,
            address=address,
            preferred_days=preferred_days,
            preferred_time=preferred_time,
        )
        messages.success(request, "Appointment booked successfully.")
        return redirect('user_profile')

    return redirect('tutor_list_chapter')

def edit_appointment_general(request, general_appointment_id):
    generalappointment = get_object_or_404(GeneralAppointment, id=general_appointment_id )

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        phone_number = request.POST.get('phone_number')
        guardian_name = request.POST.get('guardian_name')
        guardian_phone = request.POST.get('guardian_phone')
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        division = request.POST.get('division')
        district = request.POST.get('district')
        address = request.POST.get('address')
        preferred_days = request.POST.getlist('preferred_days')
        preferred_time = request.POST.getlist('preferred_time')

        generalappointment.student_name = student_name
        generalappointment.phone_number = phone_number
        generalappointment.guardian_name = guardian_name
        generalappointment.guardian_phone = guardian_phone
        generalappointment.class_name = class_name
        generalappointment.subject = subject
        generalappointment.division = division
        generalappointment.district = district
        generalappointment.address = address
        generalappointment.preferred_days = preferred_days
        generalappointment.preferred_time = preferred_time

        generalappointment.save()

        messages.success(request, "Appointment updated successfully.")
        return redirect('user_profile')

    return render(request, 'edit_appointment_general.html', {
        'generalappointment': generalappointment,
    })

def edit_appointment_chapter(request, chapter_appointment_id):
    chapterappointment = get_object_or_404(ChapterAppointment, id=chapter_appointment_id )

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        phone_number = request.POST.get('phone_number')
        guardian_name = request.POST.get('guardian_name')
        guardian_phone = request.POST.get('guardian_phone')
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        chapter = request.POST.get('chapter')
        division = request.POST.get('division')
        district = request.POST.get('district')
        address = request.POST.get('address')
        preferred_days = request.POST.getlist('preferred_days')
        preferred_time = request.POST.getlist('preferred_time')

        chapterappointment.student_name = student_name
        chapterappointment.phone_number = phone_number
        chapterappointment.guardian_name = guardian_name
        chapterappointment.guardian_phone = guardian_phone
        chapterappointment.class_name = class_name
        chapterappointment.subject = subject
        chapterappointment.chapter = chapter
        chapterappointment.division = division
        chapterappointment.district = district
        chapterappointment.address = address
        chapterappointment.preferred_days = preferred_days
        chapterappointment.preferred_time = preferred_time

        chapterappointment.save()

        messages.success(request, "Appointment updated successfully.")
        return redirect('user_profile')

    return render(request, 'edit_appointment_chapter.html', {
        'chapterappointment': chapterappointment,
    })