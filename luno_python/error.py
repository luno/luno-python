"""Luno API error classes."""


class APIError(Exception):
    """Exception raised for Luno API errors."""

    def __init__(self, code, message):
        """Initialise APIError with code and message.

        :param code: Error code from the API
        :type code: str
        :param message: Error message from the API
        :type message: str
        """
        self.code = code
        self.message = message
