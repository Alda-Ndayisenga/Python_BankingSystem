import sqlite3

connection = sqlite3.connect('bank1.db')
connection.execute ("PRAGMA foreign_keys = ON")
cursor = connection.cursor()


def save_customer(customer):
    cursor.execute('''
    INSERT INTO Customers(name, surname, address, email)
    VALUES (?, ?, ?, ?)
        ''',
        (customer.Name,
         customer.Surname,
         customer.Address,
         customer.Email)
                   )

def extract_from_database(table_name, what_to_extract):
    cursor.execute(f'''
    SELECT {what_to_extract}
    FROM {table_name}
    ORDER BY {what_to_extract} DESC
    LIMIT 1
    ''')

    result = cursor.fetchone()[0]
    return result


def save_account(account):
    cursor.execute('''
    INSERT INTO Accounts(customer_id, account_type, balance)
    VALUES (?, ?, ?)
    ''',
    (account.customer.customer_id,
     account.Account_type,
     account.Balance)
    )

    account.account_id = cursor.lastrowid

def record_transaction(transaction):
    cursor.execute('''
    INSERT INTO Transactions(account_id, transaction_type, amount)
    VALUES (?, ?, ?)
        ''',
        (transaction.Account.account_id,
            transaction.Transaction_type,
         transaction.Amount)
                   )

def update_balance(table_name, column_name, column_value, account_id):
    cursor.execute(f'''
    UPDATE {table_name} SET {column_name} = ? WHERE Account_id = ?''',
                   (column_value, account_id)
                   )