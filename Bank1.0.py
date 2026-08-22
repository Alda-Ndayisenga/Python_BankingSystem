from abc import ABC, abstractmethod
import sqlite3

connection = sqlite3.connect('bank.db')
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
def save_account(account):
    cursor.execute('''
    INSERT INTO Accounts(account_type, balance)
    VALUES (?, ?)
        ''',
        (account.Account_type,
         account.Balance)
                   )
def record_transaction(transaction):
    cursor.execute('''
    INSERT INTO Transactions(transaction_type, amount)
    VALUES (?, ?)
        ''',
        (transaction.Transaction_type,
         transaction.Amount)
                   )

class Customer:
    def __init__(self):
        self.Name = ""
        self.Surname = ""
        self.Address = ""
        self.Email = ""

    def _customer_registration(self):
        self.Name = input("Client's name: ")
        self.Surname = input("Client's surname: ")
        self.Address = input("Client's Address: ")
        self.Email = input("Client's email: ")
        while "@" not in self.Email:
            print("Invalid email address")
            self.Email = input("Client's email: ")

    def profile_creation(self):
        self._customer_registration()

    def customer_summary(self):
        print(f"""Here are the customer's details:
         Name = {self.Name}
         Surname = {self.Surname}
         Address = {self.Address}
         Email = {self.Email}
                    """)

customer1 = Customer()
customer1.profile_creation()
save_customer(customer1)
connection.commit()

class AccountTransactions:
    def __init__(self, account=None, transaction_type=None, amount=0.0):
        self.Account = account
        self.Transaction_type = transaction_type
        self.Amount = amount

    def display_transaction(self):
        print(f'{type(self.Account).__name__} | {self.Transaction_type} : {self.Amount}')

class BankAccount(ABC):
    def __init__(self, customer, Balance=0.0):
        self.customer = customer
        self._Balance = Balance
        self.Transaction_hist = []

    def deposit(self, amount):
        if amount > 0:
            self._Balance = self._Balance + amount
            print(f"You deposited {amount}; your new balance is {self._Balance}")
            transaction = AccountTransactions(account = self, transaction_type = "Deposit", amount = amount)
            self.Transaction_hist.append(transaction)
        else:
            print("Your deposit must be greater than 0")

    @abstractmethod
    def withdraw(self, amount):
        pass

    @property
    def Balance(self):
        return self._Balance


class SavingsAccount(BankAccount):
    def __init__(self, customer, Balance=0.0, min_balance=50):
        super().__init__(customer, Balance)
        self.min_balance = min_balance
        self.Account_type = "Savings Account"

    def withdraw(self, amount):
        if self._Balance > self.min_balance and amount <= (self._Balance - self.min_balance) and amount > 0:
            self._Balance = self._Balance - amount
            print(f"Your withdrew {amount}; your balance is {self._Balance}")
            transaction = AccountTransactions(account=self, transaction_type="Withdraw", amount=amount)
            self.Transaction_hist.append(transaction)
        else:
            print("Insufficient balance")

class CurrentAccount(BankAccount):
    def __init__(self, customer, Balance=0.0, min_balance=0.0):
        super().__init__(customer, Balance)
        self.min_balance = min_balance
        self.Account_type = "Current Account"

    def withdraw(self, amount):
        if amount <= self._Balance and amount > 0:
            self._Balance = self._Balance - amount
            print(f"You withdrew {amount}; your balance is {self._Balance}")
            transaction = AccountTransactions(account=self, transaction_type="Withdraw", amount=amount)
            self.Transaction_hist.append(transaction)

        else:
            print("Insufficient balance")


def withdrawing_money(account, amount=0):
    account.withdraw(amount)

def transfer(sender, receiver, amount):
    if sender == receiver:
        print("Money has to be transferred to a different account")
        print("Transfer failed!")
    else:
        sender_balance = sender.Balance
        withdrawing_money(sender, amount)
        #checking if the withdraw worked before proceeding with the deposit /that way, transfer reliably knows
        if sender.Balance == sender_balance - amount:
            print(f"{amount} has been withdrawn from {type(sender).__name__}")
            receiver_balance = receiver.Balance
            receiver.Deposit(amount)
            if receiver.Balance == receiver_balance + amount:
                print(f"{amount} has been sent to {type(receiver).__name__}")
                print("Transfer succeeded!")
                transaction_out = AccountTransactions(account = sender, transaction_type = "Transfer out", amount = amount)
                transaction_in = AccountTransactions(account = receiver, transaction_type = "Transfer in", amount = amount)
                sender.Transaction_hist.append(transaction_out)
                receiver.Transaction_hist.append(transaction_in)
            else:
                print("Transfer was canceled, try again!")


def account_creation():
    selected_account = None
    account1 = None
    account_type = input("""Account type (select the letter):
            A. Savings Account
            B. Current Account
            """).strip().upper()
    if account_type == "A":
        selected_account = "Savings Account"
        account1 = SavingsAccount(customer1)
    elif account_type == "B":
        selected_account = "Current Account"
        account1 = CurrentAccount(customer1)
    else:
        print("Invalid input")

    def account_summary():
        print(f'Account type = {selected_account}')

    def full_summary():
        customer1.customer_summary()
        account_summary()

    full_summary()
    return account1

account1 = account_creation()
save_account(account1)
connection.commit()

account1.deposit(200)
record_transaction(account1.Transaction_hist[-1])
connection.commit()
withdrawing_money(account1, 100)
record_transaction(account1.Transaction_hist[-1])
connection.commit()

for transaction in account1.Transaction_hist:
    transaction.display_transaction()

connection.close()
