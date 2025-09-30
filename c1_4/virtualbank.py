from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Sequence,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from time import time
from Crypto.Hash import MD5

CONN_STRING = "sqlite:///:memory:"
VB_CONN = create_engine(CONN_STRING)
base = declarative_base()


class Account(base):
    __tablename__ = "vb_accounts"

    acc_id = Column(Integer, Sequence("vb_accounts_acc_id_seq"), primary_key=True)
    acc_ctime = Column(DateTime, default=datetime.now(), nullable=False)
    acc_name = Column(String(100), nullable=False)
    acc_nat_id = Column(String(12), nullable=False)
    acc_code = Column(String(8), nullable=False)
    acc_age = Column(Integer, nullable=False)
    acc_amount = Column(Float, nullable=False)
    acc_pass = Column(String(100), nullable=False)
    acc_active = Column(Boolean, default=True, nullable=False)
    acc_last_login = Column(DateTime)


class Transaction(base):
    __tablename__ = "vb_transactions"

    tx_id = Column(Integer, Sequence("vb_transactions_tx_id_seq"), primary_key=True)
    tx_ctime = Column(DateTime, default=datetime.now(), nullable=False)
    tx_ref = Column(String(10), nullable=False)
    tx_account = Column(Integer, ForeignKey("vb_accounts.acc_id"), nullable=False)
    tx_type = Column(String(40), nullable=False)
    tx_amount = Column(Float, nullable=False)
    tx_narrative = Column(String, nullable=False)


base.metadata.create_all(VB_CONN)


class VirtualBank:
    # constructor
    def __init__(self):
        # create a session
        Session = sessionmaker(bind=VB_CONN)
        self.session = Session()
        # set virtual bank version
        self.version = 3.1

    # menu functions
    def mainMenu(self):
        menuStr = "Please select an option:\n1. Register\n2. Login\n3. Exit\n: "
        try:
            return int(input(menuStr))
        except ValueError:
            # input was not an integer; force invalid input
            return -1

    def userMenu(self):
        menuStr = "Please select an option:\n1. Check Balance\n2. Deposit Funds\n3. Withdraw Funds\n4. Transfer Funds\n5. Last 5 transactions\n6. Change Name\n7. Logout\n: "
        try:
            return int(input(menuStr))
        except ValueError:
            # input was not an integer; force invalid input
            return -1

    # utility functions
    def generateCode(self, seed):
        refTmp = str(time()).split(".")[1]
        return f"TX{seed}{refTmp[4:]}"

    # user functions
    def registerUser(self):
        # get the user details
        # =========================================================================
        name = input("Please enter your full name: ")
        # validate name
        while len(name) < 5:
            print("Your name must be at least 5 characters long!")
            name = input("Please enter your full name: ")
        age = input("Please enter your age in years: ")
        # validate age
        while (not age.isnumeric()) or (int(age) < 18) or (int(age) > 140):
            print("Your age must be a number between 18 and 140")
            age = input("Please enter your age in years: ")
        nationalID = input("Please enter your social security number: ")
        # validate social security
        while len(nationalID) != 12 or (not nationalID.isnumeric()):
            print("Your social security must be a number 12 digits long")
            nationalID = input("Please enter your social security number: ")
        balance = input("Please enter your initial account balance: ")
        # validate balance
        while (
            (not balance.isnumeric())
            or (int(balance) < 500)
            or (int(balance) > 99999999)
        ):
            print("Your balance must be a number between 500 and 99,999,999")
            balance = input("Please enter your initial account balance: ")
        passwd = input("Please enter a password for your account: ")
        # validate password
        while len(passwd) < 5:
            print("Your password must be at least 5 characters long!")
            passwd = input("Please enter a password for your account: ")
        # ==========================================================================
        # save record to accounts tables
        account = Account(
            acc_name=name,
            acc_nat_id=nationalID,
            acc_code=f"BOK-CCC",
            acc_age=int(age),
            acc_amount=float(balance),
            acc_pass=passwd,
        )
        # add to session
        self.session.add(account)
        # save changes
        self.session.commit()
        # get the new ID and generate the code
        result = self.session.query(Account).filter_by(acc_code="BOK-CCC").first()
        accNo = str(result.acc_id).zfill(3)
        result.acc_code = f"BOK-{accNo}"
        # save changes
        self.session.commit()
        # save deposit transaction to ledger dictionary
        ref = self.generateCode(age)
        transaction = Transaction(
            tx_ref=ref,
            tx_account=result.acc_id,
            tx_type="Deposit",
            tx_amount=float(balance),
            tx_narrative="Opening balance at account creation",
        )
        # add to session
        self.session.add(transaction)
        # save changes
        self.session.commit()
        print(f"Registered successfully. Your account number is {result.acc_code}")

    def loginUser(self):
        # ask for credentials and login
        accNo = input("Please enter your account number: ")
        passwd = input("Please enter your password: ")
        # check whether account code exists
        result = self.session.query(Account).filter_by(acc_code=accNo).first()
        if result == None:
            print("Invalid account number")
            return (False, 0)
        else:
            if result.acc_pass != passwd:
                print("Invalid password")
                return (False, 0)
            else:
                print(
                    f"Successfully logged in!\nWelcome to Virtual Bank {self.version} {result.acc_name}"
                )
                return (True, result)

    # account functions
    def checkBalance(self):
        # check balance
        print(f"Your balance is {self.loggedInAcc.acc_amount} SEK")

    def depositFunds(self):
        # make a deposit
        amount = input("Please enter an amount to deposit: ")
        # validate amount
        while (not amount.isnumeric()) or (int(amount) < 500) or (int(amount) > 999999):
            print("Your deposit amount must be a number between 500 and 999,999")
            amount = input("Please enter an amount to deposit: ")
        # can be safely converted to int
        amount = int(amount)
        # save to accounts
        self.loggedInAcc.acc_amount += amount
        # save to ledger
        ref = self.generateCode(self.loggedInAcc.acc_id)
        timeStamp = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
        transaction = Transaction(
            tx_ref=ref,
            tx_account=self.loggedInAcc.acc_id,
            tx_type="Deposit",
            tx_amount=float(amount),
            tx_narrative=f"User deposit at {timeStamp}",
        )
        # add to session
        self.session.add(transaction)
        # save changes
        self.session.commit()
        print(f"You successfully deposited {amount} SEK")

    def withdrawFunds(self):
        # make a withdrawal
        amount = input("Please enter an amount to withdraw: ")
        # validate amount
        while (not amount.isnumeric()) or (int(amount) < 500) or (int(amount) > 999999):
            print("Your withdrawal amount must be a number between 500 and 999,999")
            amount = input("Please enter an amount to withdraw: ")
        # can be safely converted to int
        amount = int(amount)
        if amount > self.loggedInAcc.acc_amount:
            print(
                f"Insufficient funds to withdraw {amount} SEK, your balance is {self.loggedInAcc.acc_amount} SEK"
            )
        else:
            # save to accounts
            self.loggedInAcc.acc_amount -= amount
            # save to ledger
            ref = self.generateCode(self.loggedInAcc.acc_id)
            timeStamp = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
            transaction = Transaction(
                tx_ref=ref,
                tx_account=self.loggedInAcc.acc_id,
                tx_type="Withdrawal",
                tx_amount=float(amount),
                tx_narrative=f"User withdrawal at {timeStamp}",
            )
            # add to session
            self.session.add(transaction)
            # save changes
            self.session.commit()
            print(f"You successfully withdrew {amount} SEK")

    def transferFunds(self):
        # make a transfer
        amount = input("Please enter an amount to transfer: ")
        # validate amount
        while (not amount.isnumeric()) or (int(amount) < 500) or (int(amount) > 999999):
            print("Your transfer amount must be a number between 500 and 999,999")
            amount = input("Please enter an amount to transfer: ")
        # can be safely converted to int
        amount = int(amount)
        if amount > self.loggedInAcc.acc_amount:
            print(
                f"Insufficient funds to transfer {amount} SEK, your balance is {self.loggedInAcc.acc_amount} SEK"
            )
        else:
            # ask for recipient
            rxcode = input("Please enter the recipient account number: ")
            rx = self.session.query(Account).filter_by(acc_code=rxcode).first()
            if rx == None:
                print("Invalid account number")
            else:
                # save to accounts
                self.loggedInAcc.acc_amount -= amount
                rx.acc_amount += amount
                # save to ledger
                ref1 = self.generateCode(self.loggedInAcc.acc_id)
                ref2 = self.generateCode(rx.acc_id)
                timeStamp = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
                transaction_tx = Transaction(
                    tx_ref=ref1,
                    tx_account=self.loggedInAcc.acc_id,
                    tx_type="Outgoing Transfer",
                    tx_amount=float(amount),
                    tx_narrative=f"User transfer to {rx.acc_name} at {timeStamp}",
                )
                transaction_rx = Transaction(
                    tx_ref=ref2,
                    tx_account=rx.acc_id,
                    tx_type="Incoming Transfer",
                    tx_amount=float(amount),
                    tx_narrative=f"{self.loggedInAcc.acc_name} transfer to user at {timeStamp}",
                )
                # add to session
                self.session.add(transaction_tx)
                self.session.add(transaction_rx)
                # save changes
                self.session.commit()
                print(f"You successfully transferred {amount} SEK to {rx.acc_name}")

    def lastTransactions(self, cutOff):
        # show last cutOff transactions
        cutOff *= -1
        ledger = (
            self.session.query(Transaction)
            .filter_by(tx_account=self.loggedInAcc.acc_id)
            .order_by(Transaction.tx_ctime)
        )
        for t in ledger[cutOff:]:
            # display the transaction
            print(f"{t.tx_ref}: {t.tx_type} of {t.tx_amount} SEK. [{t.tx_narrative}]")

    def editName(self):
        # edit the name of the account holder
        name = input("Please enter your full name: ")
        # validate name
        while len(name) < 5:
            print("Your name must be at least 5 characters long!")
            name = input("Please enter your full name: ")
        # save the new name
        self.loggedInAcc.acc_name = name
        self.session.commit()
        print(f"You successfully changed your account name to {name}")

    def editPwd(self):
        # edit the password of the account holder
        passwd = input("Please enter your current password: ")
        # validate password
        while MD5.new(passwd.encode("utf-8")).hexdigest() != self.loggedInAcc.acc_pass:
            print("Invalid password")
            passwd = input("Please enter your current password: ")
        # here we have the valid password; ask for new password
        passwd = input("Please enter your new password: ")
        # save the new password
        self.loggedInAcc.acc_pass = MD5.new(passwd.encode("utf-8")).hexdigest()
        self.session.commit()
        print(f"You successfully changed your account password")

    def userLoop(self):
        # user while loop
        uchoice = self.userMenu()
        while uchoice != 7:
            # process selection
            if uchoice == 1:
                self.checkBalance()
            elif uchoice == 2:
                self.depositFunds()
            elif uchoice == 3:
                self.withdrawFunds()
            elif uchoice == 4:
                self.transferFunds()
            elif uchoice == 5:
                self.lastTransactions(5)
            elif uchoice == 6:
                self.editName()
            else:
                # invalid entry
                print("Invalid option")
            # get the next selection
            uchoice = self.userMenu()
        print(f"Goodbye {self.loggedInAcc.acc_name}")

    # main while loop
    def mainLoop(self):
        choice = self.mainMenu()
        while choice != 3:
            # process choice
            if choice == 1:
                # register a new user
                self.registerUser()
            elif choice == 2:
                # login
                result = self.loginUser()
                if result[0] == True:
                    # main user loop
                    self.loggedInAcc = result[1]
                    self.userLoop()
            else:
                # invalid entry
                print("Invalid option")
            # get the next choice
            choice = self.mainMenu()
        print("Virtual Bank is now closed.")


if __name__ == "__main__":
    newBank = VirtualBank()
    newBank.mainLoop()
