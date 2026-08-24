import sqlite3

connection = sqlite3.connect('bank.db')
connection.execute ("PRAGMA foreign_keys = ON")
cursor = connection.cursor()

def extract_from_db(table_name, what_to_extract=None, column_name=None, column_value=None):
    cursor.execute(f'''
    SELECT {what_to_extract} FROM {table_name} WHERE {column_name} = ?''',
                   (column_value,)
                   )
    result = cursor.fetchone()
    return result[0]

customer_id1 = extract_from_db("Customers", what_to_extract="Customer_id", column_name="Email", column_value="alda@gmail.com")
customer_id2 = extract_from_db("Customers", what_to_extract="Customer_id", column_name="Email", column_value="andy@gmail.com")
customer_id3 = extract_from_db("Customers", what_to_extract="Customer_id", column_name="Email", column_value="emma@gmail.com")


def put_in_db_table(table_name, column_name1, column_name2, column_value, new_value):
    cursor.execute(f'''
    UPDATE {table_name} SET {column_name1} = ? WHERE {column_name2} = ?''',
                   (new_value, column_value)
                   )
    return 0
first_account = put_in_db_table("Accounts", "Customer_id", "Account_id", "1", customer_id1)
second_account = put_in_db_table("Accounts", "Customer_id", "Account_id", "2", customer_id2)
third_account = put_in_db_table("Accounts", "Customer_id", "Account_id", "3", customer_id3)

connection.commit()
connection.close()