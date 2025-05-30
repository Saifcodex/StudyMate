from .models import *
from .forms import  UserProfileForm, UserForm  , RegisterForm , LoginForm
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.shortcuts import render, get_object_or_404, redirect

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
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    general_appointments = GeneralAppointment.objects.filter(user=request.user)
    chapter_appointments = ChapterAppointment.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-order_date')[:5]

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

    else:
        profile_form = UserProfileForm(instance=user_profile)
        user_form = UserForm(instance=request.user)        

    context = {
        'user_profile': user_profile,
        'profile_form': profile_form,
        'user_form': user_form,
        'general_appointments': general_appointments,
        'chapter_appointments': chapter_appointments,
        'orders': orders,
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

    generaltutors = GeneralTutor.objects.all()


    if specialty:
        generaltutors = generaltutors.filter(specialty__icontains=specialty)
    if gender:
        generaltutors = generaltutors.filter(gender__iexact=gender)
    if medium:
        generaltutors = generaltutors.filter(medium__icontains=medium)
    if division:
        generaltutors = generaltutors.filter(division__icontains=division)
    if district:
        generaltutors = generaltutors.filter(district__icontains=district)
    if background:
        generaltutors = generaltutors.filter(background__icontains=background)


    approved_appointments = GeneralAppointment.objects.filter(
        generaltutor__in=generaltutors, status='Approved'
    ).values_list('generaltutor_id', 'preferred_time')


    tutor_approved_time_map = {}
    for tutor_id, time_id in approved_appointments:
        tutor_approved_time_map.setdefault(tutor_id, set()).add(time_id)


    tutor_slots = {}
    for tutor in generaltutors:
        approved_times = GeneralAppointment.objects.filter(
            generaltutor=tutor, status='Approved'
        ).values_list('preferred_time', flat=True)

        available_times = TimeSlot.objects.filter(tutor=tutor).exclude(id__in=approved_times)
        tutor_slots[tutor.id] = [
            {"id": slot.id, "time": slot.time.strftime("%I:%M %p")}
            for slot in available_times
        ]

    return render(request, 'tutor_list_general.html', {
        'generaltutors': generaltutors,
        'tutor_slots': tutor_slots,
        'tutor_slots_json': json.dumps(tutor_slots, cls=DjangoJSONEncoder),
        'specialty': dict(GeneralTutor.SPECIALTY_CHOICES).get(specialty, 'All'),
    })

def tutor_list_chapter(request):
    specialty = request.GET.get('specialty')
    gender = request.GET.get('gender')
    medium = request.GET.get('medium')
    division = request.GET.get('division')
    district = request.GET.get('district')
    background = request.GET.get('background')

    chaptertutors = ChapterTutor.objects.all()

    if specialty:
        chaptertutors = chaptertutors.filter(specialty__icontains=specialty)
    if gender:
        chaptertutors = chaptertutors.filter(gender__iexact=gender)
    if medium:
        chaptertutors = chaptertutors.filter(medium__icontains=medium)
    if division:
        chaptertutors = chaptertutors.filter(division__icontains=division)
    if district:
        chaptertutors = chaptertutors.filter(district__icontains=district)
    if background:
        chaptertutors = chaptertutors.filter(background__icontains=background)


    approved_appointments = ChapterAppointment.objects.filter(
        chaptertutor__in=chaptertutors, status='Approved'
    ).values_list('chaptertutor_id', 'preferred_time')


    tutor_approved_time_map = {}
    for tutor_id, time_id in approved_appointments:
        tutor_approved_time_map.setdefault(tutor_id, set()).add(time_id)


    tutor_slots = {}
    for tutor in chaptertutors:
        approved_times = ChapterAppointment.objects.filter(
            chaptertutor=tutor, status='Approved'
        ).values_list('preferred_time', flat=True)

        available_times = TimeSlot1.objects.filter(tutor=tutor).exclude(id__in=approved_times)
        tutor_slots[tutor.id] = [
            {"id": slot.id, "time": slot.time.strftime("%I:%M %p")}
            for slot in available_times
        ]

    return render(request, 'tutor_list_chapter.html', {
        'chaptertutors': chaptertutors,
        'tutor_slots': tutor_slots,
        'tutor_slots_json': json.dumps(tutor_slots, cls=DjangoJSONEncoder),
        'specialty': dict(ChapterTutor.SPECIALTY_CHOICES).get(specialty, 'All'),
    })

@login_required
def book_appointment_general(request, general_tutor_id):
    generaltutors = get_object_or_404(GeneralTutor, id=general_tutor_id)

    if request.method == "POST":
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
        preferred_time_id = request.POST.get('preferred_time')

        if not (phone_number and phone_number.isdigit() and len(phone_number) == 5):
            messages.error(request, "Phone number must be a 5-digit integer.")
            return redirect(request.META.get('HTTP_REFERER', 'tutor_list_general'))

        if not (guardian_phone and guardian_phone.isdigit() and len(guardian_phone) == 5):
            messages.error(request, "Guardian phone number must be a 5-digit integer.")
            return redirect(request.META.get('HTTP_REFERER', 'tutor_list_general'))

        if not preferred_time_id:
            messages.error(request, "Please choose the time from the available options.")
            return redirect(request.META.get('HTTP_REFERER', 'tutor_list_general'))

        preferred_time = get_object_or_404(TimeSlot, id=preferred_time_id)
        already_booked = GeneralAppointment.objects.filter(
            preferred_time=preferred_time,
            status='Approved'
        ).exists()

        if already_booked:
            messages.error(request, "This time slot is already booked.")
            return redirect(request.META.get('HTTP_REFERER', 'tutor_list_general'))

        GeneralAppointment.objects.create(
            user=request.user,
            generaltutor=generaltutors,
            student_name=student_name,
            phone_number=int(phone_number),
            guardian_name=guardian_name,
            guardian_phone=int(guardian_phone),
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


    generaltutors = GeneralTutor.objects.all()

    for tutor in generaltutors:
        tutor.available_slots = TimeSlot.objects.filter(tutor=tutor).exclude(
            id__in=GeneralAppointment.objects.filter(status='Approved')
            .values_list('preferred_time', flat=True)
        )

    return render(request, 'tutor_list_general.html', {
        'generaltutors': generaltutors,
    })

@login_required
def book_appointment_chapter(request, chapter_tutor_id):
    chaptertutors = get_object_or_404(ChapterTutor, id=chapter_tutor_id)
    if request.method == "POST":
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
        preferred_time_id = request.POST.get('preferred_time')

        if not (phone_number and phone_number.isdigit() and len(phone_number) == 5):
            messages.error(request, "Phone number must be a 5-digit integer.")
            return redirect(request.META.get('HTTP_REFERER', 'tutor_list_chapter'))

        if not (guardian_phone and guardian_phone.isdigit() and len(guardian_phone) == 5):
            messages.error(request, "Guardian phone number must be a 5-digit integer.")
            return redirect(request.META.get('HTTP_REFERER', 'tutor_list_chapter'))

        if not preferred_time_id:
            messages.error(request, "Please choose the time from the available options.")
            return redirect(request.META.get('HTTP_REFERER', 'tutor_list_chapter'))

        preferred_time = get_object_or_404(TimeSlot1, id=preferred_time_id)
        already_booked = ChapterAppointment.objects.filter(
            preferred_time=preferred_time,
            status='Approved'
        ).exists()

        if already_booked:
            messages.error(request, "This time slot is already booked.")
            return redirect(request.META.get('HTTP_REFERER', 'tutor_list_chapter'))

        ChapterAppointment.objects.create(
            user=request.user,
            chaptertutor=chaptertutors,
            student_name=student_name,
            phone_number=int(phone_number),
            guardian_name=guardian_name,
            guardian_phone=int(guardian_phone),
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


    chaptertutors = ChapterTutor.objects.all()

    for tutor in chaptertutors:
        tutor.available_slots = TimeSlot1.objects.filter(tutor=tutor).exclude(
            id__in=ChapterAppointment.objects.filter(status='Approved')
            .values_list('preferred_time', flat=True)
        )

    return render(request, 'tutor_list_chapter.html', {
        'chaptertutors': chaptertutors,
    })

def edit_appointment_general(request, general_appointment_id):
    general_appointment = get_object_or_404(GeneralAppointment, id=general_appointment_id)
    generaltutor = general_appointment.generaltutor

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
        preferred_days = request.POST.get('preferred_days')
        preferred_time_id = request.POST.get('preferred_time')


        if not (phone_number.isdigit() and len(phone_number) == 5):
            messages.error(request, "Phone number must be a 5-digit integer.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if not (guardian_phone.isdigit() and len(guardian_phone) == 5):
            messages.error(request, "Guardian phone number must be a 5-digit integer.")
            return redirect(request.META.get('HTTP_REFERER', '/'))


        if preferred_time_id:
            preferred_time = get_object_or_404(TimeSlot, id=preferred_time_id)
            already_booked = GeneralAppointment.objects.filter(
                preferred_time=preferred_time,
                status='Approved',
                generaltutor=generaltutor
            ).exclude(id=general_appointment.id).exists()

            if already_booked:
                messages.error(request, "This time slot is already booked.")
                return redirect(request.META.get('HTTP_REFERER', '/'))

            general_appointment.preferred_time = preferred_time
        else:
            general_appointment.preferred_time = None


        general_appointment.student_name = student_name
        general_appointment.phone_number = int(phone_number)
        general_appointment.guardian_name = guardian_name
        general_appointment.guardian_phone = int(guardian_phone)
        general_appointment.class_name = class_name
        general_appointment.subject = subject
        general_appointment.division = division
        general_appointment.district = district
        general_appointment.address = address
        general_appointment.preferred_days = preferred_days

        general_appointment.save()

        messages.success(request, "Appointment updated successfully.")
        return redirect('user_profile')


    available_times = TimeSlot.objects.filter(
        tutor=generaltutor
    ).exclude(
        id__in=GeneralAppointment.objects.filter(
            status='Approved',
            generaltutor=generaltutor
        ).exclude(id=general_appointment.id).values_list('preferred_time_id', flat=True)
    )

    return render(request, 'edit_appointment_general.html', {
        'general_appointment': general_appointment,
        'available_time_slots': available_times,
        'appointment': general_appointment,
    })



def edit_appointment_chapter(request, chapter_appointment_id):
    chapter_appointment = get_object_or_404(ChapterAppointment, id=chapter_appointment_id)
    chaptertutor = chapter_appointment.chaptertutor


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
        preferred_days = request.POST.get('preferred_days')
        preferred_time_id = request.POST.get('preferred_time')


        if not (phone_number.isdigit() and len(phone_number) == 5):
            messages.error(request, "Phone number must be a 5-digit integer.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if not (guardian_phone.isdigit() and len(guardian_phone) == 5):
            messages.error(request, "Guardian phone number must be a 5-digit integer.")
            return redirect(request.META.get('HTTP_REFERER', '/'))


        if preferred_time_id:
            preferred_time = get_object_or_404(TimeSlot1, id=preferred_time_id)
            already_booked = ChapterAppointment.objects.filter(
                preferred_time=preferred_time,
                status='Approved',
                chaptertutor=chaptertutor
            ).exclude(id=chapter_appointment.id).exists()

            if already_booked:
                messages.error(request, "This time slot is already booked.")
                return redirect(request.META.get('HTTP_REFERER', '/'))

            chapter_appointment.preferred_time = preferred_time
        else:
            chapter_appointment.preferred_time = None

        chapter_appointment.student_name = student_name
        chapter_appointment.phone_number = int(phone_number)
        chapter_appointment.guardian_name = guardian_name
        chapter_appointment.guardian_phone = int(guardian_phone)
        chapter_appointment.class_name = class_name
        chapter_appointment.subject = subject
        chapter_appointment.chapter = chapter
        chapter_appointment.division = division
        chapter_appointment.district = district
        chapter_appointment.address = address
        chapter_appointment.preferred_days = preferred_days

        chapter_appointment.save()

        messages.success(request, "Appointment updated successfully.")
        return redirect('user_profile')


    available_times = TimeSlot1.objects.filter(
        tutor=chaptertutor
    ).exclude(
        id__in=ChapterAppointment.objects.filter(
            status='Approved',
            chaptertutor=chaptertutor
        ).exclude(id=chapter_appointment.id).values_list('preferred_time_id', flat=True)
    )

    return render(request, 'edit_appointment_chapter.html', {
        'chapter_appointment': chapter_appointment,
        'available_time_slots': available_times,
        'appointment': chapter_appointment,
    })

def cancel_appointment_general(request, general_appointment_id):
    generalappointment = get_object_or_404(GeneralAppointment, id=general_appointment_id)

    generalappointment.status = 'canceled'
    generalappointment.save()

    messages.success(request, "Appointment canceled successfully.")
    return redirect('user_profile')

def cancel_appointment_chapter(request, chapter_appointment_id):
    chapterappointment = get_object_or_404(ChapterAppointment, id=chapter_appointment_id)

    chapterappointment.status = 'canceled'
    chapterappointment.save()

    messages.success(request, "Appointment canceled successfully.")
    return redirect('user_profile')


#al-amin
#books

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q  # Add this import
from .models import Book, CartItem, Order, OrderItem
from .forms import BookSearchForm, BookFilterForm

def book_list(request):
    books = Book.objects.all()
    search_form = BookSearchForm(request.GET or None)
    filter_form = BookFilterForm(request.GET or None)
    
    # Apply filters if form is valid
    if request.GET:  # If any GET parameters exist
        if filter_form.is_valid():
            data = filter_form.cleaned_data
            
            # Search query
            if data.get('query'):
                books = books.filter(
                    Q(title__icontains=data['query']) |
                    Q(author__icontains=data['query']) |
                    Q(publisher__icontains=data['query'])
                )
            
            # Category filter
            if data.get('category'):
                books = books.filter(category=data['category'])
            
            # Level filter
            if data.get('level'):
                books = books.filter(level=data['level'])
            
            # Price range
            if data.get('min_price'):
                books = books.filter(price__gte=data['min_price'])
            if data.get('max_price'):
                books = books.filter(price__lte=data['max_price'])
            
            # Bestsellers
            if data.get('bestsellers'):
                books = books.filter(is_bestseller=True)
            
            # Sorting
            if data.get('sort_by'):
                books = books.order_by(data['sort_by'])
    
    return render(request, 'book_list.html', {
        'books': books,
        'search_form': search_form,
        'filter_form': filter_form,
    })

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))  # Get the quantity from the form
    
    # Try to get the existing CartItem for this user and book
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book
    )
    
    if not created:
        # If the item already exists, update the quantity
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    return redirect('cart_view')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return redirect('book_list')  # If no items in cart, redirect to book list
    
    # Calculate total price
    total = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        # Create the order and order items
        shipping_address = request.POST.get('shipping_address', '')
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            shipping_address=shipping_address
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            # Reduce stock
            item.book.stock -= item.quantity
            item.book.save()
        
        # Clear the cart after placing the order
        cart_items.delete()
        
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'order_history.html', {'orders': orders})

# @login_required
# def user_profile(request):
#     # Fetch orders for the logged-in user
#     orders = Order.objects.filter(user=request.user).order_by('-order_date')
#     return render(request, 'user_profile.html', {'orders': orders})


#books end

#scholarship

from django.shortcuts import render
from .models import Scholarship

def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarship_list.html', {'scholarships': scholarships})

#end scholarship

#Study note

from django.shortcuts import render
from .models import StudyNote

@login_required
def study_notes(request):
    class_filter = request.GET.get('class', '')
    subject_filter = request.GET.get('subject', '')
    chapter_filter = request.GET.get('chapter', '')

    notes = StudyNote.objects.all()

    if class_filter:
        notes = notes.filter(class_name=class_filter)
    if subject_filter:
        notes = notes.filter(subject__icontains=subject_filter)
    if chapter_filter:
        notes = notes.filter(chapter_name__icontains=chapter_filter)

    context = {
        'notes': notes,
        'class_filter': class_filter,
        'subject_filter': subject_filter,
        'chapter_filter': chapter_filter,
        'class_choices': ['6', '7', '8', '9', '10', '11', '12'],  # <- Add this
    }

    return render(request, 'study_notes.html', context)

#Study notes end