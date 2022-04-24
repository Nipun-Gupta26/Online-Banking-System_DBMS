from unicodedata import category
from django.db import models

# Create your models here.
class Account : 
    accNumber = models.IntegerField()
    balance = models.IntegerField()
    category = models.CharField(max_length=45)
    customerID = models.IntegerField()
    branchID = models.IntegerField()