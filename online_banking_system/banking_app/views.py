from datetime import date
from distutils.log import error
from operator import imod
from random import randint
from unittest import result
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from banking_app.utils import *
from django.contrib import messages


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
            
            cursor.execute(query)
            row = cursor.fetchall()
            
            if len(row) == 1:
                query2 = 'select customerID,customerName,customerAddress,DOB from customer where userID = {}'.format(userID)
                cursor.execute(query2)
                temp = cursor.fetchall()
             
                if len(temp) == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    user.setUserName(temp[0][1])
                    user.setUserAddress(temp[0][2])
                    user.setDOB(temp[0][3])
                    del_cust_views()
                    cust_views(temp[0][0])
                    return redirect('home_customer')

                query3 = 'select empID,empName,empAddress,DOB, branchID from banker where userID = {} and (select userType from user where userID={}) = "banker"'.format(userID)
                cursor.execute(query3)
                temp = cursor.fetchall()
                
                if len(temp) == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    user.setUserName(temp[0][1])
                    user.setUserAddress(temp[0][2])
                    user.setDOB(temp[0][3])
                    del_banker_views()
                    banker_views(temp[0][4])
                    return redirect('home_banker')
                
                ##manager login
                query4 = 'select empID,empName,empAddress,DOB, branchID from banker where userID = {} and (select userType from user where userID={}) = "manager"'.format(userID)
                cursor.execute(query4)
                temp = cursor.fetchall()
                
                if len(temp) == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    user.setUserName(temp[0][1])
                    user.setUserAddress(temp[0][2])
                    user.setDOB(temp[0][3])
                    del_banker_views()
                    banker_views(temp[0][4])
                    return redirect('home_manager')

            else : 
                messages.error(request,'Invalid userID or password')
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
    user.setDOB('')
    user.setUserAddress('')
    user.setUserName('')
    del_cust_views()
    del_banker_views()
    return redirect('/')

def make_account(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            query1 = "select customerID from verifies where isVerified = {} and customerID in (select customerID from customer where userID = {})".format(1, user.userID) #query 1
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
                query4 = "insert into accounts values ({}, {}, '{}', {})".format(acc_num, bal, accType, branchID)
                cursor.execute(query4)
                query5 = "insert into hasAccount values ({}, {})".format(result[0][0], acc_num)
                cursor.execute(query5)
            else:
                messages.error(request, 'You have not verified your account yet')
                return redirect('/home_customer')
        return redirect('/home_customer')
    return render(request, 'customer/makeAccount.html',{'user':user})

def generate_passbook(request):
    
    context = {
        'userID': user.userID,
        'password': user.password,
        'userName': user.userName,
        'DOB': user.DOB,
        'userAddress': user.userAddress
    }
    
    with connection.cursor() as cursor:
        
        query1 = "select customerID from customer where userID = {}".format(user.userID)
        cursor.execute(query1)
        cid = cursor.fetchall()[0][0]
        query2 = "select * from transactions where accCredited not in (select accNumber from hasAccount where customerID={}) and accDebited in (select accNumber from hasAccount where customerID={})".format(cid, cid) #query 2
        query3 = "select * from transactions where accCredited in (select accNumber from hasAccount where customerID={}) and accDebited not in (select accNumber from hasAccount where customerID={})".format(cid, cid)
        query4 = "select * from transactions where accCredited in (select accNumber from hasAccount where customerID={}) and accDebited in (select accNumber from hasAccount where customerID={})".format(cid, cid)
        cursor.execute(query2)
        credit = cursor.fetchall()
        cursor.execute(query3)
        debited = cursor.fetchall()
        cursor.execute(query4)
        both = cursor.fetchall()
        context = {
            'credit': credit, 
            'debit': debited, 
            'both': both,
            'user':user
        }
        
        print(both)
        

    return render(request, 'customer/passbook.html', context)

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
            loanID = cursor.fetchall()[0][0] + 1
            query1 = "insert into loans(loanID,amount,dueDate,rate,mortgage,loanType,isVerified) values ({},{},'{}',{},'{}','{}',{})".format(loanID, amount,date_db,interestRate, mortgage, loanType, False)
            cursor.execute(query1)
           
            query2 = "insert into borrows() values ({}, {}, {})".format(loanID, 69, customerID)
            cursor.execute(query2)
        
        return redirect('/home_customer')
    return render(request, 'customer/apply_loan.html',context)

def make_transaction(request):
    
    with connection.cursor() as cursor:
        query = "select accNumber from accounts"
        cursor.execute(query)
        acc_num = cursor.fetchall()
    
    if request.method == 'POST':
        with connection.cursor() as cursor:
            accCredited = request.POST.get('accCredited', False)
            accDebited = request.POST.get('accDebited', False)
            
            if accDebited==accCredited : 
                messages.error(request, 'You cannot transfer money to yourself')
                print("You cant transfer money to yourself")
                return redirect('/home_customer')
            
            amount = int(request.POST.get('amount', False))
            password = request.POST.get('password', False)
            if password == user.password:
                query1 = "select balance from accounts where accNumber = {}".format(accCredited)
                cursor.execute(query1)
                result = cursor.fetchall()[0][0]
                balance = result
                if balance >= amount:
                    query2 = "update accounts set balance = {} where accNumber = {}".format(balance - amount, accCredited)
                    query3 = "update accounts set balance = {} where accNumber = {}".format(balance + amount, accDebited)
                    cursor.execute(query2)
                    cursor.execute(query3)
                    query4 = "select max(transactionID) from transaction"
                    cursor.execute(query4)
                    transactionID = cursor.fetchall()[0][0] + 1
                    query7 = "insert into transactions values ({}, {}, {}, {})".format(transactionID, accCredited,accDebited, amount)
                    cursor.execute(query7)
                else:
                    messages.error(request, "Amount more than Balance")
                    return redirect('/home_customer')
            else:
                messages.error(request, "Wrong Password")
                return redirect('/home_customer')
        
        return redirect('/home_customer')
    return render(request, 'customer/make_transaction.html',{'acc_num': acc_num,'user':user})

def submit_documents(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            aadharFile = request.POST.get('aadharFile', False)
            panFile = request.POST.get('panFile', False)
            passportFile = request.POST.get('passportFile', False)
            query1 = "select customerID from customer where userID = {}".format(user.userID)
            cursor.execute(query1)
            customerID = cursor.fetchall()[0][0]
            query2 = "insert into documents values ({}, '{}', '{}')".format(customerID, 'Aadhar card', aadharFile)
            cursor.execute(query2)
            query3 = "insert into documents values ({}, '{}', '{}')".format(customerID, 'Pan card', panFile)
            cursor.execute(query3)
            query4 = "insert into documents values ({}, '{}', '{}')".format(customerID, 'Passport', passportFile)
            cursor.execute(query4)
            query5 = "select max(verificationID) from verifies"
            cursor.execute(query5)
            verificationID = cursor.fetchall()[0][0] + 1
            query6 = "insert into verifies values ({}, {}, {})".format(verificationID, customerID, 0)
            cursor.execute(query6)
        return redirect('/home_customer')
    return render(request, 'customer/submit_documents.html',{'user':user,})

def check_credit_score(request):
    with connection.cursor() as cursor : 
        query = "select creditScore from customer where userID = {}".format(user.userID)
        cursor.execute(query)
        result = cursor.fetchall()
        
    
    return render(request, 'customer/check_credit_score.html',{'user':user, 'creditScore':result[0][0]})


#banker functions
def approveLoans(request) : 
    
    with connection.cursor() as cursor : 
      
            query = 'select loanID,amount,dueDate,rate,mortgage,loanType from loans where isVerified = {} and loanID in (select loanID from customer inner join borrows on customer.customerID = borrows.customerID and creditScore>5.0)'.format(0) #query 3
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

def check_loan_profile(request,loanID) : 
    
    with connection.cursor() as cursor :
        if request.method == 'POST':
            query = 'update loan set isVerified = {} where loanID = {}'.format(1,loanID)
            cursor.execute(query)
            return redirect('/home_banker')
        query = 'select customerID,customerName,customerAddress,DOB,creditScore from customer where customerID in (select customerID from borrows where loanID = {})'.format(loanID) #query 4
        cursor.execute(query)
        result = cursor.fetchall()
        
        loan = []
        loan.append(result[0][0])
        loan.append(result[0][1])
        loan.append(result[0][2])
        loan.append(result[0][3])
        loan.append(result[0][4])
        
    return render(request, 'banker/check_profile_loan_approval.html',{'userName':user.userName,'loan':loan})


def verify_documents(request):
    doc = dict()
    with connection.cursor() as cursor:
                    
        query1 = "select customerID, documentType, documentFile from documents where customerID in (select customerID from verifies where isVerified = {}) and documentType='{}'".format(0,"Aadhar card")
        cursor.execute(query1)
        result = cursor.fetchall()
        
        for i in result: 
            if i[0] in doc.keys():
                doc[i[0]].append(i[2])
            else:   
                doc[i[0]] = [i[2]]
                
       
        query1 = "select customerID, documentType, documentFile from documents where customerID in (select customerID from verifies where isVerified = {}) and documentType='{}'".format(0,"Pan card")
        cursor.execute(query1)
        result = cursor.fetchall()
   
        for i in result: 
            if i[0] in doc.keys():
                doc[i[0]].append(i[2])
            else:   
                doc[i[0]] = [i[2]]
        
        query1 = "select customerID, documentType, documentFile from documents where customerID in (select customerID from verifies where isVerified = {}) and documentType='{}'".format(0,"Passport")
        cursor.execute(query1)
        result = cursor.fetchall()
      
        for i in result: 
            if i[0] in doc.keys():
                doc[i[0]].append(i[2])
            else:   
                doc[i[0]] = [i[2]]
        
        print(doc)
        context = {
            'doc':doc,
            'user':user,
        }
    return render(request, 'banker/verify_documents.html',context)



def document_profile(request,customerID):
    context = {}
    with connection.cursor() as cursor:
        if request.method == 'POST':
            query1 = "update verifies set isVerified = {} where customerID = {}".format(1, customerID)
            cursor.execute(query1)
            return redirect('/home_banker')
        query2 = "select customer.customerID, customerName, customerAddress, DOB, documentType, documentFile from customer inner join documents on customer.customerID = documents.customerID where customer.customerID = {}".format(customerID)
        cursor.execute(query2)
        result = cursor.fetchall()
        doc = []
        for x in result[0]:
            doc.append(x)
        context = {
            'user':user,
            'doc':doc
        }
    return render(request, 'banker/document_profile.html',context)

def view_active_loans(request):
    context = {}
    with connection.cursor() as cursor:
        query1 = "select customer.customerID, customerName, loans.loanID, amount, dueDate, rate, loanType from customer inner join borrows on customer.customerID = borrows.customerID inner join loans on borrows.loanID = loans.loanID" #query 5
        cursor.execute(query1)
        result = cursor.fetchall()
        arr = []
        for x in result:
            temp = []
            temp.append(x[0])
            temp.append(x[1])
            temp.append(x[2])
            temp.append(x[3])
            temp.append(x[4])
            temp.append(x[5])
            temp.append(x[6])
            arr.append(temp)
        context = {
            'loan_list':arr,
            'user':user
        }
    return render(request, 'banker/view_active_loans.html',context)

        
def view_accounts(request):
    context = {}
    with connection.cursor() as cursor:
        query = "select branchID from banker where userID = {}".format(user.userID)
        cursor.execute(query)
        result = cursor.fetchall()
        branchID = result[0][0]
        query1 = "select customer.customerID, customerName, hasAccount.accNumber, category, balance from customer inner join hasAccount on customer.customerID = hasAccount.customerID inner join accounts on hasAccount.accNumber = accounts.accNumber where accounts.branchID = {}".format(branchID) #query 6
        cursor.execute(query1)
        result = cursor.fetchall()
        arr = []
        for x in result:
            temp = []
            temp.append(x[0])
            temp.append(x[1])
            temp.append(x[2])
            temp.append(x[3])
            temp.append(x[4])
            arr.append(temp)
            context = { 
                'account_list':arr,
                'user':user
            }
    return render(request, 'banker/view_accounts.html',context)
        

def stats(request) : 
    context = {}
    with connection.cursor() as cursor : 
        query = 'select count(*) from customer where creditScore > 5.0'
        cursor.execute(query)
        result = cursor.fetchall()
        customer_count = result[0][0]
        query2 = 'select count(*) from account where balance > 10000'
        cursor.execute(query2)
        result = cursor.fetchall()
        acc_count = result[0][0]
        query3 = 'select max(balance) from account'
        cursor.execute(query3)
        result = cursor.fetchall()
        max_bal = result[0][0]
        
        context = {
            'user':user,
            'customer_count':customer_count,
            'account_count':acc_count,
            'max_bal':max_bal
        }
        
    return render(request, 'banker/stats.html',context)

### manager view
def check_account_in_branch(request):
    context={}
    if request.method=="POST" : 
        with connection.cursor as cursor :
            branchID = request.POST.get('branchID')
            ##fill query 
            query ="select customer.customerID, customerName, hasAccount.accNumber, category, balance from customer inner join hasAccount on customer.customerID = hasAccount.customerID inner join accounts on hasAccount.accNumber = accounts.accNumber where accounts.branchID = {}".format(branchID)
            cursor.execute(query)
            result = cursor.fetchall()
            arr = []
            for x in result:
                temp = []
                temp.append(x[0])
                temp.append(x[1])
                temp.append(x[2])
                temp.append(x[3])
                temp.append(x[4])
            arr.append(temp)
            context = { 
                'account_list':arr,
                'user':user
            }
            return render(request, 'manager/list_account.html',context)
        
    return render('check_account.html',{'user':user})


def home_manager(request):
    context = {
        'user':user
    }
    return render(request, 'manager/home_manager.html', context)