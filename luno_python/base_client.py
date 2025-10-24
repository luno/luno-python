"""Base HTTP client for Luno API."""

import json
import platform

import requests

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from . import VERSION
from .error import APIError

DEFAULT_BASE_URL = "https://api.luno.com"
DEFAULT_TIMEOUT = 10
PYTHON_VERSION = platform.python_version()
SYSTEM = platform.system()
ARCH = platform.machine()


class BaseClient:
    """Base HTTP client for making authenticated requests to the Luno API."""

    def __init__(self, base_url="", timeout=0, api_key_id="", api_key_secret=""):
        """Initialise the base client.

        :type base_url: str
        :type timeout: float
        :type api_key_id: str
        :type api_key_secret: str
        """
        self.set_auth(api_key_id, api_key_secret)
        self.set_base_url(base_url)
        self.set_timeout(timeout)

        self.session = requests.Session()

    def set_auth(self, api_key_id, api_key_secret):
        """Set the API key and secret for authentication.

        :type api_key_id: str
        :type api_key_secret: str
        """
        self.api_key_id = api_key_id
        self.api_key_secret = api_key_secret

    def set_base_url(self, base_url):
        """Set the base URL for API requests.

        :type base_url: str
        """
        if base_url == "":
            base_url = DEFAULT_BASE_URL
        self.base_url = base_url.rstrip("/")

    def set_timeout(self, timeout):
        """Set the timeout in seconds for API requests.

        :type timeout: float
        """
        if timeout == 0:
            timeout = DEFAULT_TIMEOUT
        self.timeout = timeout

    def do(self, method, path, req=None, auth=False):
        """Perform an API request and return the response.

        TODO: Handle 429s.

        :type method: str
        :type path: str
        :type req: object
        :type auth: bool
        """
        if req is None:
            params = None
        else:
            try:
                params = json.loads(json.dumps(req))
            except TypeError as e:
                msg = "luno: request parameters must be JSON-serializable: %s"
                raise TypeError(msg % str(e)) from e
        headers = {"User-Agent": self.make_user_agent()}
        args = dict(timeout=self.timeout, params=params, headers=headers)
        if auth:
            args["auth"] = (self.api_key_id, self.api_key_secret)
        url = self.make_url(path, params)
        res = self.session.request(method, url, **args)
        try:
            e = res.json()
            if "error" in e and "error_code" in e:
                raise APIError(e["error_code"], e["error"])
            return e
        except JSONDecodeError:
            raise Exception("luno: unknown API error (%s)" % res.status_code)

    def make_url(self, path, params):
        """Construct the full URL for an API request.

        :type path: str
        :rtype: str
        """
        if params:
            for k, v in params.items():
                path = path.replace("{" + k + "}", str(v))
        return self.base_url + "/" + path.lstrip("/")

    def make_user_agent(self):
        """Generate the User-Agent string for API requests.

        :rtype: str
        """
        return f"LunoPythonSDK/{VERSION} python/{PYTHON_VERSION} {SYSTEM} {ARCH}"
