from django.urls import path
from .views import HomeView, CsvFileView

urlpatterns = [
    path("home", HomeView.as_view(), name="home"),
    path("parse/<int:id>", CsvFileView.as_view(), name="parse"),
]
