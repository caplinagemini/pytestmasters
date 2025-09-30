from ..welcomeIgniters import *
from unittest.mock import patch, Mock, MagicMock
import pytest, re
from unittest.mock import patch, Mock, MagicMock


def test_say_hello():
    assert re.search("ignite$", say_hello("ignite"))


def test_return_welcome_message():
    assert welcomeMessage() == "Welcome Igniters!"


def test_magic_number():
    assert magic_number(4, 5) == -2.7777777777777777


def test_is_even():
    number1 = 5
    number2 = 6
    assert is_even(number1) == False
    assert is_even(number2) == True


def test_reverse_string():
    assert reverse_string("ignite") == "etingi"
    assert reverse_string("1234") == "4321"


class TestPlusOne:
    def test_plus_one_positive(self):
        assert plus_one(1) == 2
        assert plus_one(5) == 6

    def test_plus_one_negative(self):
        assert not plus_one(1) == 3
        assert not plus_one(5) == 7


class TestException:
    def test_uppercase_string(self):
        with pytest.raises(TypeError):
            uppercase_string(1)

    def test_magic_number_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            magic_number(0, 0)

    def test_is_even_nan(self):
        with pytest.raises(TypeError) as excinfo:
            is_even("hello")

        assert excinfo.type is TypeError
        assert excinfo.type is not ZeroDivisionError


@pytest.mark.parametrize(
    "taste, size, texture, is_spicy, shape, expected",
    [
        (
            "Chocolate",
            "Big",
            "Soft",
            False,
            "Circle",
            1,
        ),
        (
            "Raspberry",
            "lagom",
            "Chewy",
            True,
            "Circle",
            2,
        ),
        (
            "Matcha",
            "Even bigger",
            "Gooey",
            False,
            "Square",
            3,
        ),
    ],
)
def test_cookie(taste, size, texture, is_spicy, shape, expected):
    cookie = Cookie(taste, size, texture, is_spicy, shape)
    assert cookie.get_info() == expected


@pytest.mark.xfail(reason="1 != 2")
def test_fancy():
    assert 1 == 2, "2 != 1"


@pytest.mark.ignite
def test_ignite():
    assert True == True


def test_magicmock():
    cookie = MagicMock(spec=Cookie)
    cookie.eat = MagicMock(return_value="yummy")
    assert cookie.eat() == "yummy"

    cookie.get_info.return_value = "abc"
    assert cookie.get_info() == "abc"


def test_send_email():
    with patch.object(EmailSender, "send_email", return_value=True) as mock_send:
        sender = EmailSender()
        result = sender.send_email("test@example.com", "Subject", "Body")
        assert result is True
        mock_send.assert_called_once_with("test@example.com", "Subject", "Body")


def test_get_inbox_count():
    with patch.object(EmailSender, "get_inbox_count", return_value=5) as mock_get:
        sender = EmailSender()
        result = sender.get_inbox_count("me")
        assert result is 5
        mock_get.assert_called_once


def test_delete_email():
    with patch.object(EmailSender, "delete_email", return_value=True) as mock_delete:
        sender = EmailSender()
        result = sender.delete_email("test@example.com")
        assert result is True
        mock_delete.assert_called_once_with("test@example.com")
