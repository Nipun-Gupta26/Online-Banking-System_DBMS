from datetime import date
from random import randint
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from pandas import array
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
                
                
                arr = []
                
                for i in range(len(result)):
                    temp = []
                    
                    temp.append(result[i][0])
                    temp.append(result[i][1])
                    temp.append(result[i][2])
                    temp.append(result[i][3])
                    temp.append(result[i][4])
                    temp.append(result[i][5])
                    
                    arr.append(temp)
                    
            
                
                context = {
                    'loan_list': arr,
                    'user':user
                }

    return render(request, 'banker/approve_loans.html',context)



def generate_passbook(request):
    
    context = {
        'userID': user.userID,
        'password': user.password,
        'userName': user.userName,
        'DOB': user.DOB,
        'userAddress': user.userAddress
    }
    
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
    
    context = {
        'userID': user.userID,
        'password': user.password,
        'userName': user.userName,
        'DOB': user.DOB,
        'userAddress': user.userAddress
    }
    
    with connection.cursor() as cursor:
        query1 = "select amount, dueDate, rate, mortagage, loanType from loans"
        cursor.execute(query1)
        result = cursor.fetchall()
        context = {
            'loans': result
        }
    return render(request, 'customer/activeLoans.html', context)

def apply_loan(request):
    
    context = {
        'userID': user.userID,
        'password': user.password,
        'userName': user.userName,
        'DOB': user.DOB,
        'userAddress': user.userAddress
    }
    
    if request.method == 'POST':
        with connection.cursor() as cursor:
            
            temp = "select customerID from customer where userID = {}".format(user.userID)
            cursor.execute(temp)
            customerID = cursor.fetchall()[0][0]
            amount = request.POST.get('amount', False)
            mortgage = request.POST.get('mortgage', False)
            loanType = request.POST.get('loanType', False)
            interestRate = 7
            
            date_db = date.today()
            
            query1 = "select max(loanID) from loan"
            cursor.execute(query1)
            
            print(mortgage)
            print(loanType)
            print(amount)
            
            
            loanID = cursor.fetchall()[0][0] + 1
            query1 = "insert into loan(loanID,amount,dueDate,rate,mortgage,loanType,isVerified) values ({},{},'{}',{},'{}','{}',{})".format(loanID, amount,date_db,interestRate, mortgage, loanType, False)
            cursor.execute(query1)
           
            query2 = "insert into borrows() values ({}, {}, {})".format(loanID, 69, customerID)
            cursor.execute(query2)
        
        return redirect('/home_customer')
    return render(request, 'customer/apply_loan.html',context)

def make_transaction(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            accCredited = request.POST.get('accCredited', False)
            accDebited = request.POST.get('accDebited', False)
            amount = request.POST.get('amount', False)
            password = request.POST.get('password', False)
            if password == user.password:
                query1 = "select balance from accounts where accNumber = {}".format(accCredited)
                cursor.execute(query1)
                balance = cursor.fetchall()[0][0]
                if balance > amount:
                    query2 = "update accounts set balance = {} where accNumber = {}".format(balance - amount, accCredited)
                    query3 = "update accounts set balance = {} where accNumber = {}".format(balance + amount, accDebited)
                    cursor.execute(query2)
                    cursor.execute(query3)
                    query4 = "select max(transactionID) from transactions"
                    cursor.execute(query4)
                    transactionID = cursor.fetchall()[0][0] + 1
                    query5 = "select customerID from hasAccount where accNumber = {}".format(accDebited)
                    cursor.execute(query5)
                    cusDeb = cursor.fetchall()[0][0]
                    query6 = "select customerID from hasAccount where accNumber = {}".format(accCredited)
                    cursor.execute(query6)
                    cusCred = cursor.fetchall()[0][0]
                    query7 = "insert into transactions values ({}, {}, {}, {}, {}, {})".format(transactionID, cusCred, accCredited,accDebited, cusDeb, amount)
                    cursor.execute(query7)
                else:
                    return redirect('/home_customer')
            else:
                return redirect('/home_customer')
        return redirect('/home_customer')
    return render(request, 'customer/make_transaction.html')

def submit_documents(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            query1 = "select customerID from customer where userID = {}".format(user.userID)
            cursor.execute(query1)
            customerID = cursor.fetchall()[0][0]
            query2 = "insert into documents values ({}, {}, {})".format(customerID, "Adhaar Card", 'adhaar.jpg')
            query3 = "insert into documents values ({}, {}, {})".format(customerID, "Pan Card", 'pan.jpg')
            query4 = "insert into documents values ({}, {}, {})".format(customerID, "Passport", 'passport.jpg')
            cursor.execute(query2)
            cursor.execute(query3)
            cursor.execute(query4)
            query5 = "select max(verificationID) from verification"
            cursor.execute(query5)
            verificationID = cursor.fetchall()[0][0] + 1
            query6 = "insert into verification values ({}, {}, {})".format(verificationID, customerID, 0)
            cursor.execute(query6)
        return redirect('/home_customer')
    return render(request, 'customer/submit_documents.html')
