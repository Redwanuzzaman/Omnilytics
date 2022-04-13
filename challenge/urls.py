from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='starting-page'),
    path("download_file", views.download_file, name='download_file'),
    path("get_report", views.report, name='get_report')
]