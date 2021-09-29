from django.urls import path, include
from . import views

appname = "urlshortener"

urlpatterns = [
    path("", views.indexView, name="index"),
    path("api/", include("urlshortener.api.urls")),
]
