from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
import json


# Create your views here.
def index(request):
    context ={}
    with connection.cursor() as cursor:
        query = "select * from test where age = 20"
        cursor.execute(query)
        row = cursor.fetchall()
        print(row)
        l = []
        for x in row:
            temp = []
            for y in x:
                temp.append(y)
            l.append(temp)
        context = {
            'id': l
        }

    return render(request, 'index.html',context)