from django.db import connection

def cust_views(customerID):
    with connection.cursor() as cursor:
        query1 = "create view accounts as select * from account where accNumber in (select accNumber from hasAccount where customerID={})".format(customerID)
        query2 = "create view transactions as select * from transaction where accCredited in (select accNumber from hasAccount where customerID={}) or accDebited in (select accNumber from hasAccount where customerID={})".format(customerID, customerID)
        query3 = "create view loans as select * from loan where isVerified = {} and loanID in (select loanID from borrows where customerID = {})".format(1, customerID)
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
    return

def del_cust_views():
    with connection.cursor() as cursor:
        query1 = "drop view if exists accounts"
        query2 = "drop view if exists transactions"
        query3 = "drop view if exists loans"
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
    return

def banker_views(branchID):
    with connection.cursor() as cursor:
        query1 = "create view accounts as select * from account where branchID = {}".format(branchID)
        query2 = "create view loans as select * from loan where loanID in (select loanID from borrows where branchID = {})".format(branchID)
        cursor.execute(query1)
        cursor.execute(query2)
    return

def del_banker_views():
    with connection.cursor() as cursor:
        query1 = "drop view if exists accounts"
        query2 = "drop view if exists loans"
        cursor.execute(query1)
        cursor.execute(query2)
    return