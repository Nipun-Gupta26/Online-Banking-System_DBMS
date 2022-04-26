from unicodedata import category
from django.db import models

# Create your models here.
class Account(models.Model): 
    accNumber = models.IntegerField()
    balance = models.IntegerField()
    category = models.CharField(max_length=45)
    customerID = models.IntegerField()
    branchID = models.IntegerField()


class Comments(models.Model): 
    comment = models.TextField()