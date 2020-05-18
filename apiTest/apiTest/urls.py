"""apiTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'create-table', views.CreateTableView, basename='create-table')
router.register(r'insert-data', views.InsertDataView, basename='insert-data')
router.register(r'get-data', views.GetDataView, basename='get-data')
router.register(r'list-tables', views.ListTablesView, basename='list-tables')
router.register(r'info-table', views.InfoTableView, basename='info-table')
router.register(r'drop-table', views.DeleteTableView, basename='drop-table')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1.0/', include(router.urls)),
    path(r'rest-auth/', include('rest_auth.urls')),
    path(r'rest-auth/registration/', include('rest_auth.registration.urls')),
]
