from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(GeneralTutor)
admin.site.register(ChapterTutor)
admin.site.register(GeneralAppointment)
admin.site.register(ChapterAppointment)
admin.site.register(TimeSlot)
admin.site.register(TimeSlot1)

#scholarship
admin.site.register(Scholarship)
#study notes
admin.site.register(StudyNote)


#al-amin
#books
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_amount', 'status')
    list_filter = ('status', 'order_date')
    inlines = [OrderItemInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'author')

admin.site.register(CartItem)
admin.site.register(OrderItem)

#books end