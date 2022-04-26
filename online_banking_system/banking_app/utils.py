from django.db import connection

def cust_views(customerID):
    with connection.cursor() as cursor:
        query1 = "create view accounts as select * from account where accNumber in (select accNumber from hasAccount where customerID={})".format(customerID)
        query2 = "create view transactions as select * from transaction where (customerCredited = {} or customerDebited = {})".format(customerID, customerID)
        query3 = "create view loans as select * from loan where loanID in(select loanID from borrcustomerID = {}) and isVerified = {}".format(customerID, 1)
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