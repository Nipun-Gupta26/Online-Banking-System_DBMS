from datetime import *
from random import randint
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from banking_app.utils import *


##classes 
class curUser:
    userID = ''
    password = ''
    userName = ''
    DOB = ''
    userAddress = ''

    def setUserID(self, userID):
        self.userID = userID
    
    def setPassword(self, password):
        self.password = password
        
    def setUserName(self, userName):
        self.userName = userName
        
    def setDOB(self, DOB):
        self.DOB = DOB
        
    def setUserAddress(self, userAddress):
        self.userAddress = userAddress

# Create your views here.
    
user = curUser()

def profile(request) : 
    return render(request, 'customer/profile_customer.html', {'userID': user.userID, 'password': user.password,'userName': user.userName, 'DOB': user.DOB, 'userAddress': user.userAddress})


def loginrequest(request):
    
    if request.method == 'POST':
        
        userID = request.POST['userID']
        password = request.POST['password']
        
        with connection.cursor() as cursor:
            query = "select * from user where userID = {} and password = '{}'".format(userID, password)
            print(query)
            
            cursor.execute(query)
            row = cursor.fetchall()
            print(row, len(row))
            
            if len(row) == 1:
                query2 = 'select customerID,customerName,customerAddress,DOB from customer where userID = {}'.format(userID)
                cursor.execute(query2)
                temp = cursor.fetchall()
                print(temp)
                if len(temp) == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    user.setUserName(temp[0][1])
                    user.setUserAddress(temp[0][2])
                    user.setDOB(temp[0][3])
                    del_cust_views()
                    cust_views(temp[0][0])
                    return redirect('home_customer')

                query3 = 'select empID,empName,empAddress,DOB from banker where userID = {}'.format(userID)
                cursor.execute(query3)
                temp = cursor.fetchall()
                
                print(temp)
                if len(temp) == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    user.setUserName(temp[0][1])
                    user.setUserAddress(temp[0][2])
                    user.setDOB(temp[0][3])
                    return redirect('home_banker')

    return redirect('/')

def login(request):
    return render(request, 'login.html')

def home_customer(request):
    context = {
        'userID': user.userID,
        'password': user.password,
        'userName': user.userName,
        'DOB': user.DOB,
        'userAddress': user.userAddress
    }
    return render(request, 'customer/home_customer.html', context)

def home_banker(request) :
    context = {
        'userID': user.userID,
        'password': user.password,
        'userName': user.userName,
        'DOB': user.DOB,
        'userAddress': user.userAddress
    }
    return render(request, 'banker/home_banker.html', context)

def sign_out(request):
    user.setUserID('')
    user.setPassword('')
    del_cust_views()
    return redirect('/')

def make_account(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            
            query1 = "select customerID from verifies where isVerified = {} and customerID in (select customerID from customer where userID = {})".format(1, user.userID)
            cursor.execute(query1)
            result = cursor.fetchall()
            if len(result) == 1:
                query2 = "select max(accNumber) from account"
                cursor.execute(query2)
                acc_num = cursor.fetchall()[0][0] + 1
                bal = request.POST.get('balance', False)
                accType = request.POST.get('accType', False)
                query3 = "select branchID from branch"
                cursor.execute(query3)
                branchQ = cursor.fetchall()
                branchID = branchQ[randint(0, len(branchQ) - 1)][0]
                query4 = "insert into account values ({}, {}, '{}', {})".format(acc_num, bal, accType, branchID)
                query5 = "insert into hasAccount values ({}, {})".format(result[0][0], acc_num)
                cursor.execute(query4)
                cursor.execute(query5)
            else:
                return redirect('/home_customer')
        return redirect('/home_customer')
    return render(request, 'customer/makeAccount.html')

def approveLoans(request) : 
    if request.method == "POST" :
        
        with connection.cursor() as cursor : 
            
            query = 'select loanID,amount,dueDate,rate,mortgage,loanType from loan where isVerified = {}'.format(0)
            cursor.execute(query)
            result = cursor.fetchall()
            
            print(result)

    return render(request, 'banker/approve_loans.html')

def generate_passbook(request):
    
    context = {}
    
    with connection.cursor() as cursor:
        query1 = "select customerID from user where userID = {}".format(user.userID)
        cursor.execute(query1)
        cid = cursor.fetchall()[0][0]
        query2 = "select * from transactions where customerCredited = {} and customerDebited != {}".format(cid, cid)
        query3 = "select * from transactions where customerDebited = {} and customerCredited != {}".format(cid, cid)
        query4 = "select * from transactions where customerCredited = {} and customerDebited = {}".format(cid, cid)
        cursor.execute(query2)
        credit = cursor.fetchall()
        cursor.execute(query3)
        debited = cursor.fetchall()
        cursor.execute(query4)
        both = cursor.fetchall()
        context = {
            'credit': credit, 
            'debited': debited, 
            'both': both
        }

    return render(request, 'passbook.html', context)

def active_loans(request):
    context = {}
    with connection.cursor() as cursor:
        query1 = "select amount, dueDate, rate, mortagage, loanType from loans"
        cursor.execute(query1)
        result = cursor.fetchall()
        context = {
            'loans': result
        }
    return render(request, 'customer/activeLoans.html', context)

def apply_loan(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            temp = "select customerID from customer where userID = {}".format(user.userID)
            cursor.execute(temp)
            customerID = cursor.fetchall()[0][0]
            amount = request.POST.get('amount', False)
            mortagage = request.POST.get('mortagage', False)
            loanType = request.POST.get('loanType', False)
            query1 = "select max(loanID) from loan"
            cursor.execute(query1)
            loanID = cursor.fetchall()[0][0] + 1
            query1 = "insert into loan(loanID,amount,dueDate,rate,mortgage,loanType,isVerified) values ({}, {}, {}, {}, {}, {}, {})".format(loanID, amount, datetime.date(), 7, mortagage, loanType, 1)
            cursor.execute(query1)
            query2 = "insert into borrows(loanID,branchID,customerID) values ({}, {}, {})".format(loanID, 69, customerID)
            cursor.execute(query2)
        return redirect('/home_customer')
    return render(request, 'customer/apply_loan.html')

def make_transaction(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            accCredited = request.POST.get('accCredited', False)
            accDebited = request.POST.get('accDebited', False)
            amount = request.POST.get('amount', False)
            password = request.POST.get('password', False)
            if password == user.password:
                query1 = ""
