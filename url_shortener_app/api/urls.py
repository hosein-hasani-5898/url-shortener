from django.urls import path
from .views import ShortURLCreateAPIView, redirect_short_url

urlpatterns = [
    # API endpoint to create a new short URL
    path("shorten/", ShortURLCreateAPIView.as_view(), name="api-shorten"),

    # Endpoint to redirect from short code to original URL
    path("<str:code>/", redirect_short_url, name="redirect-short"),
]
