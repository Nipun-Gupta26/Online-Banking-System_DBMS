ALTER TABLE services
ADD FOREIGN KEY (customerID) REFERENCES customer(customerID);

ALTER TABLE customer
ADD FOREIGN KEY (userID) REFERENCES user(userID);

ALTER TABLE documents
ADD FOREIGN KEY (customerID) REFERENCES customer(customerID);

ALTER TABLE banker
ADD FOREIGN KEY (userID) REFERENCES user(userID);

ALTER TABLE account
ADD FOREIGN KEY (customerID) REFERENCES customer(customerID);

ALTER TABLE cards
ADD FOREIGN KEY (accountNUMBER) REFERENCES account(accountNUMBER);

