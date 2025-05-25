"""Defines the URL patterns for the accounts app."""

from django.urls import path, include

app_name = 'accounts'

urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    
]