from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(GeneralTutor)
admin.site.register(ChapterTutor)
admin.site.register(GeneralAppointment)
admin.site.register(ChapterAppointment)