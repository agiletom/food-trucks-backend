from django.urls import path
from . import views

urlpatterns = [
  path('food-trucks/', views.trucks, name='trucks'),
]