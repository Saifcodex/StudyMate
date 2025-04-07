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