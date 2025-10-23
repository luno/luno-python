# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Luno Python SDK**, a wrapper for the Luno API (cryptocurrency exchange platform). The package provides a Python client for interacting with Luno's REST API, supporting operations like account management, trading, fund transfers, and market data queries.

## Architecture Overview

### Core Structure

- **`luno_python/base_client.py`**: Base HTTP client class (`BaseClient`) that handles:
  - HTTP requests using the `requests` library
  - Basic auth with API key and secret
  - Error handling and JSON parsing
  - User-Agent generation
  - URL construction with parameter substitution

- **`luno_python/client.py`**: Main `Client` class extending `BaseClient`. Contains ~100+ API methods auto-generated from the Luno API specification. Each method:
  - Wraps a specific API endpoint
  - Constructs the request object with parameters
  - Calls `do()` to make the HTTP request
  - Returns the API response as a dictionary

- **`luno_python/error.py`**: Custom `APIError` exception class for handling API errors

- **`luno_python/__init__.py`**: Exports package version

### Request/Response Flow

1. User calls a method on `Client` (e.g., `get_ticker(pair='XBTZAR')`)
2. Method builds a request dict with parameters
3. Method calls `self.do(method, path, req, auth)` from `BaseClient`
4. `do()` makes HTTP request via `requests.Session`
5. `do()` parses JSON response and checks for API error codes
6. If error found, raises `APIError`; otherwise returns response dict

### API Design Patterns

- **Authentication**: HTTP Basic Auth with `api_key_id` and `api_key_secret`
- **Path parameters**: Substituted using `{param_name}` syntax in paths
- **Query parameters**: Passed via `params` in GET requests
- **Error handling**: API returns `{"error_code": "...", "error": "..."}` on errors

## Development Commands

### Setup

```bash
# Create and activate virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install package in development mode with test dependencies
pip install -e '.[test]'
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::test_client_do_basic

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=luno_python
```

### Dependencies

- **Runtime**: `requests>=2.18.4`, `six>=1.11.0`
- **Test**: `pytest`, `pytest-cov`, `requests_mock`

## Testing Approach

Tests use `requests_mock` to mock HTTP responses. The pattern:

1. Create a `Client` instance
2. Mount mock adapter to session: `adapter.register_uri(method, url, ...)`
3. Call client method and assert response

Recent additions test the `get_balances()` method with `account_id` parameter for filtering results by account.

## Git Workflow

When making changes:

1. Run `git pull` before creating a new branch
2. Branch naming: `{username}-{issue-number}-{description}`
3. Commit messages: Present tense, describe *why* not *what*
4. Example: `"client: Add account_id parameter to get_balances method"`
5. Push and create PR when ready

## Notes on Code Generation

The `client.py` file contains ~100+ methods that are auto-generated from Luno's API specification. When modifying or adding methods:

- Follow existing docstring format (includes HTTP method, path, permissions, parameter descriptions)
- Each method constructs a `req` dict with parameters and calls `self.do()`
- Type hints in docstrings use `:type param: type_name` format for Python 2 compatibility

## File Editing Requirements

Always ensure files end with a newline character. This maintains consistency with Git diffs and repository standards.
