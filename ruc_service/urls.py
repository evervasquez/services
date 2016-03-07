from django.conf.urls import url
from django.contrib import admin
from .views import Ruc_service
urlpatterns = [
    url(r'^', Ruc_service._data_Get(), name='dashboard'),
]
