from django.conf.urls import re_path
from .views import ListCreateRegionDataAPIView, ListLogAPIView


urlpatterns = [
    re_path("on-covid-19/", ListCreateRegionDataAPIView.as_view(), name="home"),
    re_path("covid-19/logs/", ListLogAPIView.as_view(), name="logs"),
]
