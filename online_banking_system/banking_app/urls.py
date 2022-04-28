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
    path('check_loan_profile/<int:loanID>', views.check_loan_profile, name='check_loan_profile'),
    path('submit_documents', views.submit_documents, name='submit_documents'),
    path('make_transaction', views.make_transaction, name='make_transaction'),
    path('verify_documents', views.verify_documents, name='verify_documents'),
    path('document_profile/<int:customerID>', views.document_profile, name='document_profile'),
    path('view_active_loans', views.view_active_loans, name='view_active_loans'),
    path('view_accounts', views.view_accounts, name='view_accounts'),
    path('check_credit_score',views.check_credit_score,name='check_credit_score'),
]