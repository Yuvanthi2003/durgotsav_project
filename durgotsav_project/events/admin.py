from django.contrib import admin
from .models import EventRegistration, EventDay

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'registration_date']
    list_filter = ['registration_date']
    search_fields = ['name', 'email', 'phone_number']

@admin.register(EventDay)
class EventDayAdmin(admin.ModelAdmin):
    list_display = ['date', 'title']
    ordering = ['date']