# encoding = UTF-8
# using namespace std
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.ls, name="d_list"),
    path("auth/", views.auth, name="authenticate"),
    path("get/", views.get, name="get")
]
