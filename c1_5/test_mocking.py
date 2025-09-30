from .system_under_test import SystemUnderTest
import pytest
from unittest.mock import patch, Mock, MagicMock
import requests


def test_fetch_data_success():
    # Mock the requests.get method to return a successful response
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: {"key": "value"})
        sut = SystemUnderTest("https://capgemini-api.zzz")
        result = sut.fetch_data("bastu")
        assert result == {"key": "value"}
        mock_get.assert_called_once_with("https://capgemini-api.zzz/bastu")


def test_fetch_data_failure():
    # Mock the requests.get method to return a failed response
    with patch("requests.get") as mock_get:
        # add side_effect to raise HTTPError when raise_for_status is called
        mock_get.return_value = Mock(
            status_code=404, raise_for_status=Mock(side_effect=requests.HTTPError)
        )
        sut = SystemUnderTest("https://capgemini-api.zzz")
        with pytest.raises(requests.HTTPError):
            sut.fetch_data("bastu")
        mock_get.assert_called_once_with("https://capgemini-api.zzz/bastu")


def test_sut_magicmock():
    # Create a MagicMock instance for SystemUnderTest
    sut = MagicMock(spec=SystemUnderTest)
    sut.fetch_data.return_value = {"key": "value"}
    # mock an imaginary method 'teleport'
    sut.teleport = MagicMock(return_value={"location": "Mars"})
    result = sut.fetch_data("bastu")
    assert result == {"key": "value"}
    sut.fetch_data.assert_called_once_with("bastu")
    # test the imaginary method 'teleport'
    location = sut.teleport()
    assert location == {"location": "Mars"}
    sut.teleport.assert_called_once()
