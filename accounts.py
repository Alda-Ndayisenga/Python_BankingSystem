from abc import ABC, abstractmethod

class AccountTransactions:
    def __init__(self, account=None, transaction_type=None, amount=0.0):
        self.Account = account
        self.Transaction_type = transaction_type
        self.Amount = amount

    def display_transaction(self, account):
        print(f'{type(self.Account).__name__} | {self.Transaction_type} : {self.Amount}')

class BankAccount(ABC):
    def __init__(self, customer, Balance=0.0, new_balance=0.0):
        self.customer = customer
        self._Balance = Balance
        self._new_balance = new_balance
        self.Transaction_hist = []

    def deposit(self, amount, add_to_transaction_hist=True):
        if amount > 0:
            self._Balance = self._Balance + amount
            print(f"You deposited {amount}; your new balance is {self._Balance}")
            if add_to_transaction_hist:
                transaction = AccountTransactions(account=self, transaction_type="Deposit", amount=amount)
                self.Transaction_hist.append(transaction)
                self._Balance = self._Balance
        else:
            print("Your deposit must be greater than 0")
        return self._Balance

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

    def withdraw(self, amount, add_to_transaction_hist=True):
        if self._Balance > self.min_balance and amount <= (self._Balance - self.min_balance) and amount > 0:
            self._Balance = self._Balance - amount
            print(f"Your withdrew {amount}; your balance is {self._Balance}")
            if add_to_transaction_hist:
                transaction = AccountTransactions(account=self, transaction_type="Withdraw", amount=amount)
                self.Transaction_hist.append(transaction)
                self._Balance = self._Balance
        else:
            print("Insufficient balance")
        return self._Balance


class CurrentAccount(BankAccount):
    def __init__(self, customer, Balance=0.0, min_balance=0.0):
        super().__init__(customer, Balance)
        self.min_balance = min_balance
        self.Account_type = "Current Account"

    def withdraw(self, amount, add_to_transaction_hist=True):
        if amount <= self._Balance and amount > 0:
            self._Balance = self._Balance - amount
            print(f"You withdrew {amount}; your balance is {self._Balance}")
            if add_to_transaction_hist:
                transaction = AccountTransactions(account=self, transaction_type="Withdraw", amount=amount)
                self.Transaction_hist.append(transaction)
                self._Balance = self._Balance
        else:
            print("Insufficient balance")
        return self._Balance

def withdrawing_money(account, amount=0, add_to_transaction_hist=True):
    account.withdraw(amount, add_to_transaction_hist)

def transfer(sender, receiver, amount):
    if sender == receiver:
        print("Money has to be transferred to a different account")
        print("Transfer failed!")
    else:
        sender_balance = sender.Balance
        withdrawing_money(sender, amount, add_to_transaction_hist=False)
        #checking if the withdraw worked before proceeding with the deposit /that way, transfer reliably knows
        if sender.Balance == sender_balance - amount:
            print(f"{amount} has been withdrawn from {type(sender).__name__}")
            # sender.Balance = sender.Balance
            receiver_balance = receiver.Balance
            receiver.deposit(amount, add_to_transaction_hist=False)
            if receiver.Balance == receiver_balance + amount:
                print(f"{amount} has been sent to {type(receiver).__name__}")
                print("Transfer succeeded!")
                # sender.Balance = sender.Balance
                transaction_out = AccountTransactions(account = sender, transaction_type = "Transfer out", amount = amount)
                transaction_in = AccountTransactions(account = receiver, transaction_type = "Transfer in", amount = amount)
                sender.Transaction_hist.append(transaction_out)
                receiver.Transaction_hist.append(transaction_in)
            else:
                print("Transfer was canceled, try again!")
            return sender.Balance, receiver.Balance


def account_creation(customer):
    selected_account = None
    account = None
    account_type = input("""Account type (select the letter):
            A. Savings Account
            B. Current Account
            """).strip().upper()
    while account_type not in ("A", "B"):
        print("Invalid input")
        account_type = input("""Account type (select the letter):
            A. Savings Account
            B. Current Account
            """).strip().upper()
    if account_type == "A":
        selected_account = "Savings Account"
        account = SavingsAccount(customer)
    elif account_type == "B":
        selected_account = "Current Account"
        account = CurrentAccount(customer)

    def account_summary(account):
        print(f'Account type = {selected_account}')

    def full_summary(customer):
        customer.customer_summary()
        account_summary(account)

    full_summary(customer)
    return account
