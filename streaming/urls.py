from django.urls import path

from .views import index, video

urlpatterns = [
    path("", index),
    path("video/", video),
]
