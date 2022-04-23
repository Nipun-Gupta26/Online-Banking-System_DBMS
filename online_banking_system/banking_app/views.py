from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection


# Create your views here.
def index(request):
    context ={}
    with connection.cursor() as cursor:
        query = "select * from test where age = 20"
        cursor.execute(query)
        row = cursor.fetchall()
        print(row)
        context = {
            'name': row[0][0],
            'age': row[0][1],
        }

    return render(request, 'index.html',context)