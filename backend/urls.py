
# backend/urls.py

from django.contrib import admin
from django.urls import path, include                 # add this
from rest_framework import routers                    # add this
        
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('foodtrucks.urls')),
]