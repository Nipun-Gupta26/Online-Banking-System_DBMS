from django import views
from django.contrib import admin
from django.urls import path
from banking_app import views

urlpatterns = [
    path('',views.login,name='login'),
    path('loginrequest', views.loginrequest, name='loginrequest'),
    path('home_customer',views.home_customer,name='home_customer'),
    path('home_banker',views.home_banker,name='home_banker'),
]