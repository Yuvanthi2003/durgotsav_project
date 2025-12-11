from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('day/<int:day_number>/', views.day_detail_view, name='day_detail'),
    path('register/', views.registration_view, name='register'),
    path('success/', views.success_view, name='success'),
]