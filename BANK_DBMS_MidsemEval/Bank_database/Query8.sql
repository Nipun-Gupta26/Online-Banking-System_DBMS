select customerNAME, customer.customerID, balence from customer, account where customerNAME like 'kip%' and customer.customerID = account.customerID and customer.customerID in(select customerID from account where balence > '$61112.05')