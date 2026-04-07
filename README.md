<img src="https://d32exi8v9av3ux.cloudfront.net/static/images/luno-email-336.png">

# Luno Python SDK

[![Run Tests](https://github.com/luno/luno-python/actions/workflows/test.yml/badge.svg)](https://github.com/luno/luno-python/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/luno-python.svg)](https://pypi.org/project/luno-python/)
[![Python Versions](https://img.shields.io/pypi/pyversions/luno-python.svg)](https://pypi.org/project/luno-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/luno/luno-python/blob/main/LICENSE.txt)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=luno_luno-python&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=luno_luno-python)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=luno_luno-python&metric=coverage)](https://sonarcloud.io/summary/new_code?id=luno_luno-python)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=luno_luno-python&metric=bugs)](https://sonarcloud.io/summary/new_code?id=luno_luno-python)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=luno_luno-python&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=luno_luno-python)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=luno_luno-python&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=luno_luno-python)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=luno_luno-python&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=luno_luno-python)

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
  print(res)
except Exception as e:
  print(e)
```

For more examples, see the [examples](./examples) folder.

### License

[MIT](https://github.com/luno/luno-python/blob/main/LICENSE.txt)
