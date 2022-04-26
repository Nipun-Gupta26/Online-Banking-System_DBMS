from django import views
from django.contrib import admin
from django.urls import path
from banking_app import views

urlpatterns = [
    path('',views.login,name='login'),
    path('loginrequest', views.loginrequest, name='loginrequest'),
    path('home_customer', views.home_customer, name='home_customer'),
    path('home_banker', views.home_banker, name='home_banker'),
    path('make_account', views.make_account, name='make_account'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('profile',views.profile,name='profile'),
    path('passbook', views.generate_passbook, name='passbook'),
    path('approve_loans',views.approveLoans,name='approve_loans'),
    path('active_loans', views.active_loans, name='active_loans'),
    path('apply_loan', views.apply_loan, name='apply_loan'),
]