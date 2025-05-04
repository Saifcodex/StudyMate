from django.urls import path
from django.views.generic import RedirectView

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/',views.faq,name='faq'),

    #Login related
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout, name='logout'),

    #  error handle
    path('custom_error/', views.custom_error, name='custom_error'),

    #General tutor
    path('tutor_list_general/', views.tutor_list_general, name='tutor_list_general'),
    path('book_appointment_general/<int:general_tutor_id>/', views.book_appointment_general, name='book_appointment_general'),
    path('edit_appointment_general/<int:general_appointment_id>/', views.edit_appointment_general, name='edit_appointment_general'),
    path('cancel_appointment_general/<int:general_appointment_id>/', views.cancel_appointment_general, name='cancel_appointment_general'),

    #Chapter Tutor
    path('tutor_list_chapter/', views.tutor_list_chapter, name='tutor_list_chapter'),
    path('book_appointment_chapter/<int:chapter_tutor_id>/', views.book_appointment_chapter, name='book_appointment_chapter'),
    path('edit_appointment_chapter/<int:chapter_appointment_id>/', views.edit_appointment_chapter, name='edit_appointment_chapter'),
    path('cancel_appointment_chapter/<int:chapter_appointment_id>/', views.cancel_appointment_chapter, name='cancel_appointment_chapter'),
    # path('books/', views.book_list, name='book_list'),

    #scholarship
    path('scholarships/', views.scholarship_list, name='scholarship_list'),
    #Study notes
    path('study-notes/', views.study_notes, name='study_notes'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)