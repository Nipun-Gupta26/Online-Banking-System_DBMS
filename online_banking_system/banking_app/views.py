from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect


# Create your views here.
class curUser:
    userID = ''
    password = ''

    def setUserID(self, userID):
        self.userID = userID
    
    def setPassword(self, password):
        self.password = password
    
user = curUser()

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
                query2 = 'select count(*) from customer where userID = {}'.format(userID)
                cursor.execute(query2)
                temp = cursor.fetchall()
                print(temp)
                if temp[0][0] == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    return redirect('/home_customer')

                query3 = 'select count(*) from banker where userID = {}'.format(userID)
                cursor.execute(query3)
                temp = cursor.fetchall()
                if temp[0][0] == 1:
                    user.setUserID(userID)
                    user.setPassword(password)
                    return redirect('/home_banker')

    return redirect('/')

def login(request):
    return render(request, 'login.html')
