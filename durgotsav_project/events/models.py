

from django.db import models

class EventRegistration(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5, default='+91')
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    selected_events = models.JSONField(default=list)  # This should be here
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.email}"

class EventDay(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.date} - {self.title}"