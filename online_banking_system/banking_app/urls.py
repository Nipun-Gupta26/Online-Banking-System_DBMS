from django import views
from django.contrib import admin
from django.urls import path
from banking_app import views

urlpatterns = [
    path('',views.index,name='index'),
    # path('contact',views.contact,name='contact'),
]