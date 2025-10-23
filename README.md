<img src="https://d32exi8v9av3ux.cloudfront.net/static/images/luno-email-336.png">

# Luno API [![Build Status](https://travis-ci.org/luno/luno-python.svg?branch=master)](https://travis-ci.org/luno/luno-python)

This Python package provides a wrapper for the [Luno API](https://www.luno.com/api).

### Installation

```
pip install luno-python
```

### Authentication

Please visit the [Settings](https://www.luno.com/wallet/settings/api_keys) page
to generate an API key.

### Example usage

```python
from luno_python.client import Client

c = Client(api_key_id='key_id', api_key_secret='key_secret')
try:
  res = c.get_ticker(pair='XBTZAR')
  print res
except Exception as e:
  print e
```

### License

[MIT](https://github.com/luno/luno-python/blob/master/LICENSE.txt)
