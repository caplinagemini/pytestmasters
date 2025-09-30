from .code_to_test import divide, recursion, add, raises_value_error
import pytest

# normal assertions
def test_add():
    assert add(2, 3) == 5


# exception assertions
def test_divide_by_zero():
    # check for a specific exception
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_recursion_depth():
    # check for a specific exception text
    with pytest.raises(RuntimeError) as excinfo:

        recursion()
    assert "maximum recursion" in str(excinfo.value)


def test_exception_subclasses():
    # ZeroDivisionError is a subclass of ArithmeticError
    with pytest.raises(ArithmeticError):
        divide(1, 0)


def test_specific_subclass():
    with pytest.raises(ArithmeticError) as excinfo:
        divide(1, 0)

    assert excinfo.type is ZeroDivisionError
    assert excinfo.type is not FloatingPointError


def test_value_error_message():
    # check for a specific message using regex
    with pytest.raises(ValueError, match=r".* 0900 .*") as excinfo:
        raises_value_error()
    assert "Capgemini training" in str(excinfo.value)


# grouping tests in a class
class TestMath:
    def test_addition(self):
        assert add(1, 2) == 3

    def test_division(self):
        """Tests division"""
        assert divide(6, 2) == 3
