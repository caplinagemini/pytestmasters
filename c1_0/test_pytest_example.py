from .code_to_test import add


def test_add_function():
    assert add(2, 3) == 5
    assert add(-1, -1) == -2
    assert add(0, 0) == 0
