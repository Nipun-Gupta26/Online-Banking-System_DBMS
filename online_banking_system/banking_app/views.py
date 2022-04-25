from random import randint
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from banking_app.utils import *


##classes 
class curUser:
    userID = ''
    password = ''

    def setUserID(self, userID):
        self.userID = userID
    
    def setPassword(self, password):
        self.password = password

# Create your views here.
    
user = curUser()

def profile(request) : 
    return render(request, 'profile.html', {'userID': user.userID, 'password': user.password})

def home_customer(request):
    context = {
        'userID': user.userID,
        'password': user.password
    }
    return render(request, 'home_customer.html', context)

def home_banker(request) :
    context = {
        'userID': user.userID,
        'password': user.password
    }
    return render(request, 'home_banker.html', context)

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
                query2 = 'select customerID from customer where userID = {}'.format(userID)
                cursor.execute(query2)
                temp = cursor.fetchall()
                print(temp)
                if len(temp) == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    del_cust_views()
                    cust_views(temp[0][0])
                    return redirect('/home_customer')

                query3 = 'select empID from banker where userID = {}'.format(userID)
                cursor.execute(query3)
                temp = cursor.fetchall()
                if len(temp) == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    return redirect('/home_banker')

    return redirect('/')

def login(request):
    return render(request, 'login.html')

def home_customer(request):
    context = {
        'userID': user.userID,
        'password': user.password
    }
    return render(request, 'home_customer.html', context)

def home_banker(request) :
    context = {
        'userID': user.userID,
        'password': user.password
    }
    return render(request, 'home_banker.html', context)

def sign_out(request):
    user.setUserID('')
    user.setPassword('')
    del_cust_views()
    return redirect('/')

def make_account(request):
    with connection.cursor() as cursor:
        query1 = "select count(*) from verifies where customerID in (select customerID from customer where userID = {}) and isVerified = {}".format(user.userID, 1)
        cursor.execute(query1)
        result = cursor.fetchall()
        if result[0][0] == 1:
            query2 = "select max(accNumber) from account"
            cursor.execute(query2)
            acc_num = cursor.fetchnall()[0][0] + 1
            bal = request.POST['balance']
            accType = request.POST['accType']
            query3 = "select branchID from branch"
            cursor.execute(query3)
            result = cursor.fetchall()
            branchID = result[randint(0, len(result) - 1)][0]
            query4 = "insert into account values ({}, {}, {}, {})".format(acc_num, bal, accType, branchID)
            cursor.execute(query4)
        return 
