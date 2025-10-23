# Contributing

## Clone

```bash
git clone https://github.com/luno/luno-python.git
```

## Create Virtual env

 ```bash
cd luno-python
python -m venv env
source env/bin/activate
```

## Install Dependencies

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -e '.[dev]'
```

This installs the package in editable mode with all development dependencies including testing tools and pre-commit hooks.

## Set Up Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to maintain code quality and consistency. The hooks run automatically before commits and pushes.

### Install the git hook scripts

```bash
pre-commit install
```

This will run code formatting, linting, security checks, and tests on every commit.

### Run hooks manually

To run all hooks on all files manually:

```bash
pre-commit run --all-files
```

### What the hooks do

- **Code formatting**: Automatically formats code with `black` and sorts imports with `isort`
- **Linting**: Checks code quality with `flake8`
- **Security**: Scans for common security issues with `bandit`
- **File checks**: Fixes trailing whitespace, ensures files end with newlines, validates YAML/JSON
- **Tests**: Runs the full test suite (via `pytest`)

### Skip hooks (use sparingly)

If you need to skip hooks for a specific commit:

```bash
git commit --no-verify
```

## Run Tests

```bash
pytest
```
