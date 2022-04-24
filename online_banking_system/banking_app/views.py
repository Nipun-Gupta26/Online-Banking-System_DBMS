from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
import json

from requests import session

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

def home(request):
    context = {
        'userID': user.userID,
        'password': user.password
    }
    return render(request, 'home.html', context)

def loginrequest(request):
    if request.method == 'POST':
        
        userID = request.POST['userID']
        password = request.POST['password']
        
        with connection.cursor() as cursor:
            
            query = "select * from test where userID = {} and password = '{}'".format(userID, password)
            print(query)
            
            cursor.execute(query)
            row = cursor.fetchall()
            print(row, len(row))
            
            if len(row) == 1:
                user.setUserID(userID)
                user.setPassword(password)
                return redirect('home')
            else:
                return redirect('login')

def login(request):
    return render(request, 'login.html')
