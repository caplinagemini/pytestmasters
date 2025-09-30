# example code to be tested
class Account:
    def __init__(self, name, code, initial_balance=0.0):
        self.name = name
        self.code = code
        self.active = False
        self.balance = initial_balance

    def activate(self):
        self.active = True

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


class Transaction:
    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def process(self):
        if self.amount > 0:
            self.account.deposit(self.amount)
        else:
            self.account.withdraw(-self.amount)
