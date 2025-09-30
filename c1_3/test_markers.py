from .code_to_test import Car
import pytest
import sys


@pytest.mark.parametrize(
    "model, year, top_speed, powertrain, expected_info",
    [
        (
            "Toyota Corolla",
            2020,
            180,
            "petrol",
            "2020 Toyota Corolla with petrol powertrain and a top speed of 180 km/h",
        ),
        (
            "Volvo EX90",
            2025,
            250,
            "electric",
            "2025 Volvo EX90 with electric powertrain and a top speed of 250 km/h",
        ),
        (
            "Ford Mustang",
            2019,
            240,
            "petrol",
            "2019 Ford Mustang with petrol powertrain and a top speed of 240 km/h",
        ),
        (
            "Nissan Leaf",
            2022,
            150,
            "electric",
            "2022 Nissan Leaf with electric powertrain and a top speed of 150 km/h",
        ),
    ],
)
def test_car_get_info(model, year, top_speed, powertrain, expected_info):
    car = Car(model, year, top_speed, powertrain)
    assert car.get_info() == expected_info


@pytest.mark.skip(reason="Skipping this test for demonstration purposes")
def test_skipped():
    assert False, "This test should be skipped"


@pytest.mark.skipif(sys.version_info > (3, 6), reason="requires python3.6 or lower")
def test_function_3_6():
    assert True, "This test runs only on Python 3.6 or lower"


@pytest.mark.xfail(reason="This test is expected to fail for demonstration purposes")
def test_expected_failure():
    assert 1 + 1 == 3, "This test is expected to fail"


@pytest.mark.fancy
def test_fancy():
    assert 1 + 1 == 2, "This test is fancy"
