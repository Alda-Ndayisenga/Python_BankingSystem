import database
from bank_registration import Customer
from accounts import transfer, account_creation


customer = Customer()
customer.profile_creation()
database.save_customer(customer)
customer.customer_id = database.cursor.lastrowid
customer.customer_id = database.extract_from_database("Customers", "Customer_id")

account = account_creation(customer)
account.account_id = database.extract_from_database("Accounts", "Account_id")
database.save_account(account)
account.account_id = database.cursor.lastrowid
database.connection.commit()


customer1 = Customer()
customer1.profile_creation()
database.save_customer(customer1)
customer1.customer_id = database.cursor.lastrowid
customer1.customer_id = database.extract_from_database("Customers", "Customer_id")

account1 = account_creation(customer1)
account1.account_id = database.extract_from_database("Accounts", "Account_id")
database.save_account(account1)
account1.account_id = database.cursor.lastrowid
database.connection.commit()


balance_after_dep = account.deposit(200)
database.record_transaction(account.Transaction_hist[-1])
database.update_balance("Accounts", "Balance", balance_after_dep, account.account_id)
database.connection.commit()


balance_after_transf_out, balance_after_transf_in = transfer(account, account1, 100)
database.record_transaction(account.Transaction_hist[-1])
database.update_balance("Accounts", "Balance", balance_after_transf_out, account.account_id)
database.record_transaction(account1.Transaction_hist[-1])
database.update_balance("Accounts", "Balance", balance_after_transf_in, account1.account_id)


balance_after_with = account1.withdraw(50)
database.record_transaction(account1.Transaction_hist[-1])
database.update_balance("Accounts", "Balance", balance_after_with, account1.account_id)
database.connection.commit()

database.connection.close()

for transaction in account.Transaction_hist:
    transaction.display_transaction(account)

for transaction in account1.Transaction_hist:
    transaction.display_transaction(account1)