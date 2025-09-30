from .virtualbank import *
from io import StringIO
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from unittest.mock import patch


@pytest.fixture
def bank():
    engine = create_engine("sqlite:///:memory:")
    base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    bank = VirtualBank()
    bank.session = session
    return bank


@pytest.fixture(autouse=True)
def accounts(bank):
    account1 = Account(
        acc_name="Bob",
        acc_nat_id=1111_1111_1111,
        acc_code=f"BOK-001",
        acc_age=25,
        acc_amount=9999.99,
        acc_pass="bobpass",
    )
    account2 = Account(
        acc_name="Alice",
        acc_nat_id=2222_2222_2222,
        acc_code=f"BOK-002",
        acc_age=30,
        acc_amount=5000.00,
        acc_pass="alicepass",
    )
    account3 = Account(
        acc_name="Charlie",
        acc_nat_id=3333_3333_3333,
        acc_code=f"BOK-003",
        acc_age=35,
        acc_amount=7500.50,
        acc_pass="charliepass",
    )
    bank.session.add(account1)
    bank.session.add(account2)
    bank.session.add(account3)
    bank.session.commit()


@pytest.fixture(autouse=True)
def transactions(bank):
    account1 = bank.session.query(Account).filter_by(acc_code="BOK-001").first()
    account2 = bank.session.query(Account).filter_by(acc_code="BOK-002").first()
    account3 = bank.session.query(Account).filter_by(acc_code="BOK-003").first()

    tx1 = Transaction(
        tx_ref="TX1001",
        tx_account=account1.acc_id,
        tx_type="deposit",
        tx_amount=1000.00,
        tx_narrative="Initial deposit",
    )
    tx2 = Transaction(
        tx_ref="TX1002",
        tx_account=account1.acc_id,
        tx_type="withdrawal",
        tx_amount=200.00,
        tx_narrative="ATM withdrawal",
    )
    tx3 = Transaction(
        tx_ref="TX2001",
        tx_account=account2.acc_id,
        tx_type="deposit",
        tx_amount=500.00,
        tx_narrative="Paycheck",
    )
    tx4 = Transaction(
        tx_ref="TX3001",
        tx_account=account3.acc_id,
        tx_type="transfer",
        tx_amount=250.00,
        tx_narrative="Transfer to Alice",
    )
    bank.session.add_all([tx1, tx2, tx3, tx4])
    bank.session.commit()


class TestInterface:
    def test_test(self, bank):
        result = bank.session.query(Account).filter_by(acc_code="BOK-001").first()
        print(result.acc_name)

    def test_main_menu(self, bank):
        with patch("builtins.input", return_value="2"):
            assert bank.mainMenu() == 2

    def test_main_menu_nan(self, bank):
        with patch("builtins.input", return_value="a"):
            assert bank.mainMenu() == -1

    @pytest.mark.xfail(
        reason="Any integer input is accepted, main loop will handle invalid options"
    )
    def test_main_menu_out_of_range(self, bank):
        with patch("builtins.input", return_value="5"):
            assert bank.mainMenu() == -1

    def test_main_menu_newline(self, bank):
        with patch("builtins.input", return_value=""):
            assert bank.mainMenu() == -1


class TestUser:
    def test_register_user(self, bank):
        name = "Kalle"
        age = "25"
        nationalID = "123456789000"
        balance = "7777"
        password = "12345"
        items = [name, age, nationalID, balance, password]
        items_iter = iter(items)
        with patch("builtins.input", lambda _: next(items_iter)):
            bank.registerUser()
        result = bank.session.query(Account).filter_by(acc_name="Kalle").first()
        assert result.acc_age == 25
        assert result.acc_nat_id == "123456789000"
        assert result.acc_amount == 7777
        assert result.acc_pass == "12345"


class TestTransactions:
    def test_transfer_fund(self, bank):
        amount = "560"
        recipient = "BOK-002"
        items = [amount, recipient]
        items_iter = iter(items)
        aUser = bank.session.query(Account).filter_by(acc_name="Bob").first()
        oldAmount = aUser.acc_amount
        bank.loggedInAcc = aUser
        with patch("builtins.input", lambda _: next(items_iter)):
            bank.transferFunds()
        assert (
            oldAmount - float(amount)
            == bank.session.query(Account).filter_by(acc_name="Bob").first().acc_amount
        )
