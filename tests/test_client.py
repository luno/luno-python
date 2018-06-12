import pytest
import requests
import requests_mock

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from luno_python.client import Client
from luno_python.error import APIError


def test_client():
    c = Client()
    c.set_auth('api_key_id', 'api_key_secret')
    c.set_base_url('base_url')
    c.set_timeout(10)

    assert c.api_key_id == 'api_key_id'
    assert c.api_key_secret == 'api_key_secret'
    assert c.base_url == 'base_url'
    assert c.timeout == 10


def test_client_do_basic():
    c = Client()
    c.set_base_url('mock://test/')

    adapter = requests_mock.Adapter()
    c.session.mount('mock', adapter)

    adapter.register_uri('GET', 'mock://test/', text='ok')
    with pytest.raises(Exception):
        res = c.do('GET', '/')

    adapter.register_uri('GET', 'mock://test/', text='{"key":"value"}')
    res = c.do('GET', '/')
    assert res['key'] == 'value'

    adapter.register_uri('GET', 'mock://test/', text='{}', status_code=400)
    res = c.do('GET', '/')  # no exception, because no error present

    adapter.register_uri('GET', 'mock://test/',
                         text='{"error_code":"code","error":"message"}',
                         status_code=400)
    with pytest.raises(APIError) as e:
        res = c.do('GET', '/')
    assert e.value.code == 'code'
    assert e.value.message == 'message'
