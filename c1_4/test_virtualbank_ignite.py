from .virtualbank import Account, VirtualBank, Transaction
from io import StringIO
import pytest


@pytest.fixture(autouse=True)
def bank():
    return VirtualBank()


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

    def test_main_menu(self, bank, monkeypatch):
        input = StringIO("2\n")
        monkeypatch.setattr("sys.stdin", input)
        assert bank.mainMenu() == 2

    def test_main_menu_nan(self, bank, monkeypatch):
        input = StringIO("a\n")
        monkeypatch.setattr("sys.stdin", input)
        assert bank.mainMenu() == -1

    @pytest.mark.xfail(
        reason="Any integer input is accepted, main loop will handle invalid options"
    )
    def test_main_menu_out_of_range(self, bank, monkeypatch):
        input = StringIO("5\n")
        monkeypatch.setattr("sys.stdin", input)
        assert bank.mainMenu() == -1

    def test_main_menu_newline(self, bank, monkeypatch):
        input = StringIO("\n")
        monkeypatch.setattr("sys.stdin", input)
        assert bank.mainMenu() == -1


class TestUser:
    def test_register_user(self, bank, monkeypatch):
        name = "Kalle"
        age = 25
        nationalID = 123456789000
        balance = 7777
        password = 12345
        input = StringIO(f"{name}\n{age}\n{nationalID}\n{balance}\n{password}\n")
        monkeypatch.setattr("sys.stdin", input)
        bank.registerUser()
        result = bank.session.query(Account).filter_by(acc_name="Kalle").first()
        assert result.acc_age == 25
        assert result.acc_nat_id == "123456789000"
        assert result.acc_amount == 7777
        assert result.acc_pass == "12345"


class TestTransactions:
    1
