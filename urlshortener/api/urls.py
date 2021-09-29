from django.urls import path
from .views import UrlshortenerListView, UrlshortenerDetailView, RedirectorView

app_name = "api"

urlpatterns = [
    path("<str:short_url>", RedirectorView.as_view(), name="redirect_url"),
    path("list-url/", UrlshortenerListView.as_view(), name="list_url"),
    path(
        "detail-url/<int:url_id>/",
        UrlshortenerDetailView.as_view(),
        name="detail_url",
    ),
]
