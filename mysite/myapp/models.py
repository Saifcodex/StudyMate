from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class UserProfile(models.Model):
    def __str__(self):
        return self.fullname()

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

    age = models.IntegerField()
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER)


    @receiver(pre_delete, sender=User)
    def delete_user_profile(sender, instance, **kwargs):
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.delete()
        except UserProfile.DoesNotExist:
            pass


class GeneralTutor(models.Model):
    DIVISION_CHOICES = [
        ('Barishal', 'Barishal'),
        ('Chattogram', 'Chattogram'),
        ('Dhaka', 'Dhaka'),
        ('Khulna', 'Khulna'),
        ('Mymensingh', 'Mymensingh'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangpur', 'Rangpur'),
        ('Sylhet', 'Sylhet'),
    ]
    DISTRICT_CHOICES = [
        ('Barguna', 'Barguna'),
        ('Barishal', 'Barishal'),
        ('Bhola', 'Bhola'),
        ('Jhalokati', 'Jhalokati'),
        ('Patuakhali', 'Patuakhali'),
        ('Pirojpur', 'Pirojpur'),
        ('Bandarban', 'Bandarban'),
        ('Brahmanbaria', 'Brahmanbaria'),
        ('Chandpur', 'Chandpur'),
        ('Chattogram', 'Chattogram'),
        ('Cumilla', 'Cumilla'),
        ('Cox\'s Bazar', 'Cox\'s Bazar'),
        ('Feni', 'Feni'),
        ('Khagrachhari', 'Khagrachhari'),
        ('Lakshmipur', 'Lakshmipur'),
        ('Noakhali', 'Noakhali'),
        ('Rangamati', 'Rangamati'),
        ('Dhaka', 'Dhaka'),
        ('Faridpur', 'Faridpur'),
        ('Gazipur', 'Gazipur'),
        ('Gopalganj', 'Gopalganj'),
        ('Kishoreganj', 'Kishoreganj'),
        ('Madaripur', 'Madaripur'),
        ('Manikganj', 'Manikganj'),
        ('Munshiganj', 'Munshiganj'),
        ('Narayanganj', 'Narayanganj'),
        ('Narsingdi', 'Narsingdi'),
        ('Rajbari', 'Rajbari'),
        ('Shariatpur', 'Shariatpur'),
        ('Tangail', 'Tangail'),
        ('Bagerhat', 'Bagerhat'),
        ('Chuadanga', 'Chuadanga'),
        ('Jashore', 'Jashore'),
        ('Jhenaidah', 'Jhenaidah'),
        ('Khulna', 'Khulna'),
        ('Kushtia', 'Kushtia'),
        ('Magura', 'Magura'),
        ('Meherpur', 'Meherpur'),
        ('Narail', 'Narail'),
        ('Satkhira', 'Satkhira'),
        ('Jamalpur', 'Jamalpur'),
        ('Mymensingh', 'Mymensingh'),
        ('Netrokona', 'Netrokona'),
        ('Sherpur', 'Sherpur'),
        ('Bogra', 'Bogra'),
        ('Joypurhat', 'Joypurhat'),
        ('Naogaon', 'Naogaon'),
        ('Natore', 'Natore'),
        ('Chapainawabganj', 'Chapainawabganj'),
        ('Pabna', 'Pabna'),
        ('Rajshahi', 'Rajshahi'),
        ('Sirajganj', 'Sirajganj'),
        ('Dinajpur', 'Dinajpur'),
        ('Gaibandha', 'Gaibandha'),
        ('Kurigram', 'Kurigram'),
        ('Lalmonirhat', 'Lalmonirhat'),
        ('Nilphamari', 'Nilphamari'),
        ('Panchagarh', 'Panchagarh'),
        ('Rangpur', 'Rangpur'),
        ('Thakurgaon', 'Thakurgaon'),
        ('Habiganj', 'Habiganj'),
        ('Moulvibazar', 'Moulvibazar'),
        ('Sunamganj', 'Sunamganj'),
        ('Sylhet', 'Sylhet'),
    ]
    SPECIALTY_CHOICES = [
        ('Science', 'Science'),
        ('Biology', 'Biology'),
        ('Laws', 'Laws'),
        ('Math', 'Math'),
        ('Chemistry', 'Chemistry'),
        ('Physics', 'Physics'),
        ('Economics', 'Economics'),
        ('History', 'History'),
        ('Sociology', 'Sociology'),
        ('English', 'English'),
        ('Politics','Politics'),
    ]
    AVAILABILITY_Status = [
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    ]
    Background_CHOICES = [('Science', 'Science'), ('Commerce', 'Commerce'), ('Arts', 'Arts'), ('Engineering', 'Engineering'),('Medical', 'Medical')]

    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MEDIUM_CHOICES = [('Bangla', 'Bangla'), ('English', 'English')]

    image = models.ImageField(upload_to='tutor_images/')
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES, default='Science')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    qualification = models.CharField(max_length=100)
    tuition_experience = models.IntegerField()
    availability = models.CharField(max_length=20, choices=AVAILABILITY_Status, db_index=True, default='Available')
    medium = models.CharField(max_length=10, choices=MEDIUM_CHOICES)
    preferred_classes = models.CharField(max_length=100,default=1)
    preferred_subjects = models.CharField(max_length=100)
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES, default='Dhaka')
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES, default='Dhaka')
    background = models.CharField(max_length=20, choices=Background_CHOICES , default='Science')
    salary_range = models.CharField(max_length=50)

    def __str__(self):
        return f"General Tutor Name : {self.name}"

class GeneralAppointment(models.Model):

    DIVISION_CHOICES = [
        ('Barishal', 'Barishal'),
        ('Chattogram', 'Chattogram'),
        ('Dhaka', 'Dhaka'),
        ('Khulna', 'Khulna'),
        ('Mymensingh', 'Mymensingh'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangpur', 'Rangpur'),
        ('Sylhet', 'Sylhet'),
    ]
    DISTRICT_CHOICES = [
        ('Barguna', 'Barguna'),
        ('Barishal', 'Barishal'),
        ('Bhola', 'Bhola'),
        ('Jhalokati', 'Jhalokati'),
        ('Patuakhali', 'Patuakhali'),
        ('Pirojpur', 'Pirojpur'),
        ('Bandarban', 'Bandarban'),
        ('Brahmanbaria', 'Brahmanbaria'),
        ('Chandpur', 'Chandpur'),
        ('Chattogram', 'Chattogram'),
        ('Cumilla', 'Cumilla'),
        ('Cox\'s Bazar', 'Cox\'s Bazar'),
        ('Feni', 'Feni'),
        ('Khagrachhari', 'Khagrachhari'),
        ('Lakshmipur', 'Lakshmipur'),
        ('Noakhali', 'Noakhali'),
        ('Rangamati', 'Rangamati'),
        ('Dhaka', 'Dhaka'),
        ('Faridpur', 'Faridpur'),
        ('Gazipur', 'Gazipur'),
        ('Gopalganj', 'Gopalganj'),
        ('Kishoreganj', 'Kishoreganj'),
        ('Madaripur', 'Madaripur'),
        ('Manikganj', 'Manikganj'),
        ('Munshiganj', 'Munshiganj'),
        ('Narayanganj', 'Narayanganj'),
        ('Narsingdi', 'Narsingdi'),
        ('Rajbari', 'Rajbari'),
        ('Shariatpur', 'Shariatpur'),
        ('Tangail', 'Tangail'),
        ('Bagerhat', 'Bagerhat'),
        ('Chuadanga', 'Chuadanga'),
        ('Jashore', 'Jashore'),
        ('Jhenaidah', 'Jhenaidah'),
        ('Khulna', 'Khulna'),
        ('Kushtia', 'Kushtia'),
        ('Magura', 'Magura'),
        ('Meherpur', 'Meherpur'),
        ('Narail', 'Narail'),
        ('Satkhira', 'Satkhira'),
        ('Jamalpur', 'Jamalpur'),
        ('Mymensingh', 'Mymensingh'),
        ('Netrokona', 'Netrokona'),
        ('Sherpur', 'Sherpur'),
        ('Bogra', 'Bogra'),
        ('Joypurhat', 'Joypurhat'),
        ('Naogaon', 'Naogaon'),
        ('Natore', 'Natore'),
        ('Chapainawabganj', 'Chapainawabganj'),
        ('Pabna', 'Pabna'),
        ('Rajshahi', 'Rajshahi'),
        ('Sirajganj', 'Sirajganj'),
        ('Dinajpur', 'Dinajpur'),
        ('Gaibandha', 'Gaibandha'),
        ('Kurigram', 'Kurigram'),
        ('Lalmonirhat', 'Lalmonirhat'),
        ('Nilphamari', 'Nilphamari'),
        ('Panchagarh', 'Panchagarh'),
        ('Rangpur', 'Rangpur'),
        ('Thakurgaon', 'Thakurgaon'),
        ('Habiganj', 'Habiganj'),
        ('Moulvibazar', 'Moulvibazar'),
        ('Sunamganj', 'Sunamganj'),
        ('Sylhet', 'Sylhet'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generalappointments')
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')]

    generaltutor = models.ForeignKey(GeneralTutor, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    class_name = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100)
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES, default='Dhaka')
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES, default='Dhaka')
    address = models.CharField(max_length=100)
    preferred_days = models.CharField(max_length=100)
    preferred_time = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Student Name : {self.student_name} - General Teacher Name : {self.generaltutor.name}"

class ChapterTutor(models.Model):
        DIVISION_CHOICES = [
            ('Barishal', 'Barishal'),
            ('Chattogram', 'Chattogram'),
            ('Dhaka', 'Dhaka'),
            ('Khulna', 'Khulna'),
            ('Mymensingh', 'Mymensingh'),
            ('Rajshahi', 'Rajshahi'),
            ('Rangpur', 'Rangpur'),
            ('Sylhet', 'Sylhet'),
        ]
        DISTRICT_CHOICES = [
            ('Barguna', 'Barguna'),
            ('Barishal', 'Barishal'),
            ('Bhola', 'Bhola'),
            ('Jhalokati', 'Jhalokati'),
            ('Patuakhali', 'Patuakhali'),
            ('Pirojpur', 'Pirojpur'),
            ('Bandarban', 'Bandarban'),
            ('Brahmanbaria', 'Brahmanbaria'),
            ('Chandpur', 'Chandpur'),
            ('Chattogram', 'Chattogram'),
            ('Cumilla', 'Cumilla'),
            ('Cox\'s Bazar', 'Cox\'s Bazar'),
            ('Feni', 'Feni'),
            ('Khagrachhari', 'Khagrachhari'),
            ('Lakshmipur', 'Lakshmipur'),
            ('Noakhali', 'Noakhali'),
            ('Rangamati', 'Rangamati'),
            ('Dhaka', 'Dhaka'),
            ('Faridpur', 'Faridpur'),
            ('Gazipur', 'Gazipur'),
            ('Gopalganj', 'Gopalganj'),
            ('Kishoreganj', 'Kishoreganj'),
            ('Madaripur', 'Madaripur'),
            ('Manikganj', 'Manikganj'),
            ('Munshiganj', 'Munshiganj'),
            ('Narayanganj', 'Narayanganj'),
            ('Narsingdi', 'Narsingdi'),
            ('Rajbari', 'Rajbari'),
            ('Shariatpur', 'Shariatpur'),
            ('Tangail', 'Tangail'),
            ('Bagerhat', 'Bagerhat'),
            ('Chuadanga', 'Chuadanga'),
            ('Jashore', 'Jashore'),
            ('Jhenaidah', 'Jhenaidah'),
            ('Khulna', 'Khulna'),
            ('Kushtia', 'Kushtia'),
            ('Magura', 'Magura'),
            ('Meherpur', 'Meherpur'),
            ('Narail', 'Narail'),
            ('Satkhira', 'Satkhira'),
            ('Jamalpur', 'Jamalpur'),
            ('Mymensingh', 'Mymensingh'),
            ('Netrokona', 'Netrokona'),
            ('Sherpur', 'Sherpur'),
            ('Bogra', 'Bogra'),
            ('Joypurhat', 'Joypurhat'),
            ('Naogaon', 'Naogaon'),
            ('Natore', 'Natore'),
            ('Chapainawabganj', 'Chapainawabganj'),
            ('Pabna', 'Pabna'),
            ('Rajshahi', 'Rajshahi'),
            ('Sirajganj', 'Sirajganj'),
            ('Dinajpur', 'Dinajpur'),
            ('Gaibandha', 'Gaibandha'),
            ('Kurigram', 'Kurigram'),
            ('Lalmonirhat', 'Lalmonirhat'),
            ('Nilphamari', 'Nilphamari'),
            ('Panchagarh', 'Panchagarh'),
            ('Rangpur', 'Rangpur'),
            ('Thakurgaon', 'Thakurgaon'),
            ('Habiganj', 'Habiganj'),
            ('Moulvibazar', 'Moulvibazar'),
            ('Sunamganj', 'Sunamganj'),
            ('Sylhet', 'Sylhet'),
        ]
        SPECIALTY_CHOICES = [
            ('Science', 'Science'),
            ('Biology', 'Biology'),
            ('Laws', 'Laws'),
            ('Math', 'Math'),
            ('Chemistry', 'Chemistry'),
            ('Physics', 'Physics'),
            ('Economics', 'Economics'),
            ('History', 'History'),
            ('Sociology', 'Sociology'),
            ('English', 'English'),
            ('Politics', 'Politics'),
        ]
        AVAILABILITY_Status = [
            ('Available', 'Available'),
            ('Not Available', 'Not Available'),
        ]
        Background_CHOICES = [('Science', 'Science'), ('Commerce', 'Commerce'), ('Arts', 'Arts'),
                              ('Engineering', 'Engineering'), ('Medical', 'Medical')]

        GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
        MEDIUM_CHOICES = [('Bangla', 'Bangla'), ('English', 'English')]

        image = models.ImageField(upload_to='tutor_images/')
        name = models.CharField(max_length=100)
        specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES, default='Science')
        gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
        qualification = models.CharField(max_length=100)
        tuition_experience = models.IntegerField()
        availability = models.CharField(max_length=20, choices=AVAILABILITY_Status, db_index=True, default='Available')
        medium = models.CharField(max_length=10, choices=MEDIUM_CHOICES)
        preferred_classes = models.CharField(max_length=100, default=1)
        preferred_subjects = models.CharField(max_length=100)
        division = models.CharField(max_length=20, choices=DIVISION_CHOICES, default='Dhaka')
        district = models.CharField(max_length=20, choices=DISTRICT_CHOICES, default='Dhaka')
        background = models.CharField(max_length=20, choices=Background_CHOICES, default='Science')
        chapter = models.CharField(max_length=100)
        salary_per_chapter = models.CharField(max_length=50)

        def __str__(self):
            return f"ChapterWise Tutor Name : {self.name}"

class ChapterAppointment(models.Model):

    DIVISION_CHOICES = [
        ('Barishal', 'Barishal'),
        ('Chattogram', 'Chattogram'),
        ('Dhaka', 'Dhaka'),
        ('Khulna', 'Khulna'),
        ('Mymensingh', 'Mymensingh'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangpur', 'Rangpur'),
        ('Sylhet', 'Sylhet'),
    ]
    DISTRICT_CHOICES = [
        ('Barguna', 'Barguna'),
        ('Barishal', 'Barishal'),
        ('Bhola', 'Bhola'),
        ('Jhalokati', 'Jhalokati'),
        ('Patuakhali', 'Patuakhali'),
        ('Pirojpur', 'Pirojpur'),
        ('Bandarban', 'Bandarban'),
        ('Brahmanbaria', 'Brahmanbaria'),
        ('Chandpur', 'Chandpur'),
        ('Chattogram', 'Chattogram'),
        ('Cumilla', 'Cumilla'),
        ('Cox\'s Bazar', 'Cox\'s Bazar'),
        ('Feni', 'Feni'),
        ('Khagrachhari', 'Khagrachhari'),
        ('Lakshmipur', 'Lakshmipur'),
        ('Noakhali', 'Noakhali'),
        ('Rangamati', 'Rangamati'),
        ('Dhaka', 'Dhaka'),
        ('Faridpur', 'Faridpur'),
        ('Gazipur', 'Gazipur'),
        ('Gopalganj', 'Gopalganj'),
        ('Kishoreganj', 'Kishoreganj'),
        ('Madaripur', 'Madaripur'),
        ('Manikganj', 'Manikganj'),
        ('Munshiganj', 'Munshiganj'),
        ('Narayanganj', 'Narayanganj'),
        ('Narsingdi', 'Narsingdi'),
        ('Rajbari', 'Rajbari'),
        ('Shariatpur', 'Shariatpur'),
        ('Tangail', 'Tangail'),
        ('Bagerhat', 'Bagerhat'),
        ('Chuadanga', 'Chuadanga'),
        ('Jashore', 'Jashore'),
        ('Jhenaidah', 'Jhenaidah'),
        ('Khulna', 'Khulna'),
        ('Kushtia', 'Kushtia'),
        ('Magura', 'Magura'),
        ('Meherpur', 'Meherpur'),
        ('Narail', 'Narail'),
        ('Satkhira', 'Satkhira'),
        ('Jamalpur', 'Jamalpur'),
        ('Mymensingh', 'Mymensingh'),
        ('Netrokona', 'Netrokona'),
        ('Sherpur', 'Sherpur'),
        ('Bogra', 'Bogra'),
        ('Joypurhat', 'Joypurhat'),
        ('Naogaon', 'Naogaon'),
        ('Natore', 'Natore'),
        ('Chapainawabganj', 'Chapainawabganj'),
        ('Pabna', 'Pabna'),
        ('Rajshahi', 'Rajshahi'),
        ('Sirajganj', 'Sirajganj'),
        ('Dinajpur', 'Dinajpur'),
        ('Gaibandha', 'Gaibandha'),
        ('Kurigram', 'Kurigram'),
        ('Lalmonirhat', 'Lalmonirhat'),
        ('Nilphamari', 'Nilphamari'),
        ('Panchagarh', 'Panchagarh'),
        ('Rangpur', 'Rangpur'),
        ('Thakurgaon', 'Thakurgaon'),
        ('Habiganj', 'Habiganj'),
        ('Moulvibazar', 'Moulvibazar'),
        ('Sunamganj', 'Sunamganj'),
        ('Sylhet', 'Sylhet'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chapterappointments')
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')]

    chaptertutor = models.ForeignKey(ChapterTutor, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    class_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES, default='Dhaka')
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES, default='Dhaka')
    address = models.CharField(max_length=100)
    preferred_days = models.CharField(max_length=100)
    preferred_time = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Student Name : {self.student_name} - ChapterWise Teacher Name : {self.chaptertutor.name}"






#Scholarship

from django.db import models

class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    deadline = models.CharField(max_length=100)  # e.g. "March, 2025"
    pdf = models.FileField(upload_to='scholarship_pdfs/')

    def __str__(self):
        return self.title
    
#scholarship end

#Study Note

from django.db import models

class StudyNote(models.Model):
    CLASS_CHOICES = [
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
        ('11', 'Class 11'),
        ('12', 'Class 12'),
    ]

    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    subject = models.CharField(max_length=100)
    chapter_number = models.IntegerField()
    chapter_name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='study_notes/thumbnails/')
    pdf = models.FileField(upload_to='study_notes/pdfs/')

    def __str__(self):
        return f"{self.class_name} - {self.subject} - Chapter {self.chapter_number}: {self.chapter_name}"

#Study Note end

#al-amin
#books 

from django.utils import timezone

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('textbook', 'Textbook'),
        ('reference', 'Reference Book'),
        ('novel', 'Novel'),
        ('academic', 'Academic'),
        ('other', 'Other'),
    ]
    
    LEVEL_CHOICES = [
        ('school', 'School'),
        ('college', 'College'),
        ('university', 'University'),
        ('general', 'General'),
    ]
    
    cover_image = models.ImageField(upload_to='book_covers/')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def item_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"
    
    # books end