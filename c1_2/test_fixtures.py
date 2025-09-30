import pytest
from random import randint

from .code_to_test import Account, Transaction


@pytest.fixture
def accounts():
    return [Account("Alice", "001"), Account("Bob", "002"), Account("Charlie", "003")]


@pytest.fixture
def bank(accounts):
    bank = {}
    for account in accounts:
        account.activate()
        bank[account.code] = [
            account,
            [Transaction(account, randint(-1000, 5000)) for _ in range(5)],
        ]
    return bank


@pytest.fixture
def limits():
    return {}


@pytest.fixture(autouse=True)
def populate_limits(limits):
    limits.update(
        {
            "min_deposit": 500,
            "max_deposit": 999999,
            "min_withdraw": 100,
            "max_withdraw": 1000000,
        }
    )
    return limits


def test_account_activation(accounts, limits):
    # use the accounts fixture
    for account in accounts:
        assert not account.active
        account.activate()

    assert all(account.active for account in accounts)
    # show auto-use fixture
    assert limits["min_deposit"] == 500


def test_transactions(bank, limits):
    # use the bank fixture which itself uses accounts fixture
    for code, (account, transactions) in bank.items():
        if code == "limits":
            continue
        initial_balance = account.balance
        for transaction in transactions:
            transaction.process()

        assert account.balance != initial_balance
        # show that auto-use fixture applies to all tests
        assert limits["max_withdraw"] == 1000000
