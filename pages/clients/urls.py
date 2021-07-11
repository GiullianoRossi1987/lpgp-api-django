# encoding = UTF-8
# using namespace std
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.ls, name="list"),
    path("list-enc/",views.ls_enc, name="encoded"), 
    path("access/", views.val, name="access")
]
