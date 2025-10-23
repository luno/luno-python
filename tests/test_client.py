"""Tests for the Luno Python client."""

from decimal import Decimal

import pytest
import requests_mock

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from luno_python.client import Client
from luno_python.error import APIError

# Mock response fixtures
MOCK_BALANCES_RESPONSE = {
    "balance": [
        {
            "account_id": "12345678910",
            "asset": "XBT",
            "balance": "0.00",
            "reserved": "0.00",
            "unconfirmed": "0.00",
        },
        {
            "account_id": "98765432100",
            "asset": "ETH",
            "balance": "1.50",
            "reserved": "0.10",
            "unconfirmed": "0.05",
        },
        {
            "account_id": "55555555555",
            "asset": "ZAR",
            "balance": "1000.00",
            "reserved": "0.00",
            "unconfirmed": "0.00",
        },
    ]
}

MOCK_BALANCES_RESPONSE_TWO_ACCOUNTS = {
    "balance": [
        {
            "account_id": "12345678910",
            "asset": "XBT",
            "balance": "0.00",
            "reserved": "0.00",
            "unconfirmed": "0.00",
        },
        {
            "account_id": "98765432100",
            "asset": "ETH",
            "balance": "1.50",
            "reserved": "0.10",
            "unconfirmed": "0.05",
        },
    ]
}

MOCK_BALANCES_RESPONSE_INTEGER_IDS = {
    "balance": [
        {
            "account_id": 12345678910,
            "asset": "XBT",
            "balance": "0.00",
            "reserved": "0.00",
            "unconfirmed": "0.00",
        },
        {
            "account_id": 98765432100,
            "asset": "ETH",
            "balance": "1.50",
            "reserved": "0.10",
            "unconfirmed": "0.05",
        },
    ]
}

MOCK_EMPTY_BALANCE_RESPONSE = {"balance": []}

MOCK_MALFORMED_RESPONSE = {"some_other_key": "value"}


def test_client():
    """Test client initialization and configuration."""
    c = Client()
    c.set_auth("api_key_id", "api_key_secret")
    c.set_base_url("base_url")
    c.set_timeout(10)

    assert c.api_key_id == "api_key_id"
    assert c.api_key_secret == "api_key_secret"
    assert c.base_url == "base_url"
    assert c.timeout == 10


def test_client_do_basic():
    """Test basic client do method functionality."""
    c = Client()
    c.set_base_url("mock://test/")

    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test/", text="ok")
    with pytest.raises(Exception, match="unknown API error"):
        res = c.do("GET", "/")

    adapter.register_uri("GET", "mock://test/", text='{"key":"value"}')
    res = c.do("GET", "/")
    assert res["key"] == "value"

    adapter.register_uri("GET", "mock://test/", text="{}", status_code=400)
    res = c.do("GET", "/")  # no exception, because no error present

    adapter.register_uri("GET", "mock://test/", text='{"error_code":"code","error":"message"}', status_code=400)
    with pytest.raises(APIError) as e:
        res = c.do("GET", "/")
    assert e.value.code == "code"
    assert e.value.message == "message"


def test_get_balances_without_account_id():
    """Test get_balances without account_id parameter (backward compatibility)."""
    c = Client()
    c.set_base_url("mock://test/")

    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test/api/1/balance", json=MOCK_BALANCES_RESPONSE)

    # Test without account_id - should return full response
    result = c.get_balances()
    assert result == MOCK_BALANCES_RESPONSE
    assert "balance" in result
    assert len(result["balance"]) == 3


def test_get_balances_with_valid_account_id():
    """Test get_balances with valid account_id parameter."""
    c = Client()
    c.set_base_url("mock://test/")

    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test/api/1/balance", json=MOCK_BALANCES_RESPONSE)

    # Test with valid account_id - should return single account
    result = c.get_balances(account_id="12345678910")
    expected = {
        "account_id": "12345678910",
        "asset": "XBT",
        "balance": "0.00",
        "reserved": "0.00",
        "unconfirmed": "0.00",
    }
    assert result == expected

    # Test with another valid account_id
    result = c.get_balances(account_id="98765432100")
    expected = {
        "account_id": "98765432100",
        "asset": "ETH",
        "balance": "1.50",
        "reserved": "0.10",
        "unconfirmed": "0.05",
    }
    assert result == expected


def test_get_balances_with_invalid_account_id():
    """Test get_balances with invalid account_id parameter."""
    c = Client()
    c.set_base_url("mock://test/")

    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test/api/1/balance", json=MOCK_BALANCES_RESPONSE_TWO_ACCOUNTS)

    # Test with invalid account_id - should return None
    result = c.get_balances(account_id="99999999999")
    assert result is None


def test_get_balances_with_account_id_and_assets():
    """Test get_balances with both account_id and assets parameters."""
    c = Client()
    c.set_base_url("mock://test/")

    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test/api/1/balance", json=MOCK_BALANCES_RESPONSE_TWO_ACCOUNTS)

    # Test with both parameters
    result = c.get_balances(assets=["XBT"], account_id="12345678910")
    expected = {
        "account_id": "12345678910",
        "asset": "XBT",
        "balance": "0.00",
        "reserved": "0.00",
        "unconfirmed": "0.00",
    }
    assert result == expected


def test_get_balances_with_account_id_type_conversion():
    """Test get_balances with account_id type conversion (string vs int)."""
    c = Client()
    c.set_base_url("mock://test/")

    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test/api/1/balance", json=MOCK_BALANCES_RESPONSE_INTEGER_IDS)

    # Test with string account_id when API returns integer - should work due to type conversion
    result = c.get_balances(account_id="12345678910")
    expected = {
        "account_id": 12345678910,
        "asset": "XBT",
        "balance": "0.00",
        "reserved": "0.00",
        "unconfirmed": "0.00",
    }
    assert result == expected


def test_get_balances_with_empty_balance_response():
    """Test get_balances when API returns empty balance list."""
    c = Client()
    c.set_base_url("mock://test/")

    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test/api/1/balance", json=MOCK_EMPTY_BALANCE_RESPONSE)

    # Test with account_id on empty response
    result = c.get_balances(account_id="12345678910")
    assert result is None

    # Test without account_id on empty response
    result = c.get_balances()
    assert result == MOCK_EMPTY_BALANCE_RESPONSE


def test_get_balances_with_malformed_response():
    """Test get_balances when API returns malformed response."""
    c = Client()
    c.set_base_url("mock://test/")

    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)

    adapter.register_uri("GET", "mock://test/api/1/balance", json=MOCK_MALFORMED_RESPONSE)

    # Test with account_id on malformed response
    result = c.get_balances(account_id="12345678910")
    assert result is None

    # Test without account_id on malformed response
    result = c.get_balances()
    assert result == MOCK_MALFORMED_RESPONSE


def test_client_do_with_non_serializable_params():
    """Test that non-JSON-serializable parameters raise a clear error."""
    c = Client()
    c.set_base_url("mock://test/")

    # Test with Decimal (not JSON-serializable)
    with pytest.raises(TypeError) as exc_info:
        c.do("GET", "/", req={"amount": Decimal("10.5")})
    assert "JSON-serializable" in str(exc_info.value)

    # Test with custom object (not JSON-serializable)
    class CustomObject:
        pass

    with pytest.raises(TypeError) as exc_info:
        c.do("GET", "/", req={"obj": CustomObject()})
    assert "JSON-serializable" in str(exc_info.value)

    # Test with None request (should not raise)
    adapter = requests_mock.Adapter()
    c.session.mount("mock", adapter)
    adapter.register_uri("GET", "mock://test/", json={"result": "ok"})
    result = c.do("GET", "/", req=None)
    assert result["result"] == "ok"
