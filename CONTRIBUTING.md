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

## Releasing

This project is published to [PyPI](https://pypi.org/project/luno-python/). Releases are made by maintainers with repository write access and PyPI publish access.

### Steps

1. **Decide the version number** following [Semantic Versioning](https://semver.org/):
   - Patch (`x.y.Z`): backwards-compatible bug fixes
   - Minor (`x.Y.0`): new backwards-compatible functionality
   - Major (`X.0.0`): breaking changes

2. **Bump the version** in `luno_python/__init__.py`:
   ```python
   VERSION = "x.y.z"
   ```

3. **Commit and push** the version bump on a branch, then open and merge a PR:
   ```bash
   git checkout -b release-x.y.z
   git add luno_python/__init__.py
   git commit -m "release: bump version to x.y.z"
   git push origin release-x.y.z
   gh pr create --title "release: bump version to x.y.z" --body "Bump version for release."
   # After review, merge the PR
   ```

4. **Create a GitHub Release** from the merged commit on `main`:
   ```bash
   git checkout main && git pull origin main
   gh release create vx.y.z --title "vx.y.z" --generate-notes
   ```
   This triggers the publish workflow which automatically builds and uploads the package to PyPI.

### PyPI Trusted Publishing

The publish workflow uses [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OpenID Connect), which means no API tokens need to be stored as secrets. This must be configured once in PyPI's project settings under *Publishing → Add a new publisher*, pointing at this repository's `publish.yml` workflow.
