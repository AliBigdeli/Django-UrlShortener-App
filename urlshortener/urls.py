from django.urls import path, include
from . import views

app_name = "urlshortener"

urlpatterns = [
    path("", views.indexView, name="index"),
    path("api/", include("urlshortener.api.urls")),
]
