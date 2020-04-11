"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import re_path, include
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic.base import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="Covid-19 impact estimator API",
        default_version="v1",
        description=("REST API that estimates impact of covid-19 based on user data"),
        terms_of_service="https://www.covidestmator/policies/terms/",
        contact=openapi.Contact(email="odipojames12@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path("^admin/", admin.site.urls),
    re_path("api/v1/", include("covid_estimator.urls")),
    re_path(
        "api/v1/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="api-documentation",
    ),
    re_path(
        "api/v1/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    re_path(
        "",
        RedirectView.as_view(url="api/v1/docs/", permanent=False),
        name="api_documentation",
    ),
]
