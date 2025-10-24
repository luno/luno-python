"""Setup script for luno-python package."""

from setuptools import find_packages, setup

from luno_python import VERSION

setup(
    name="luno-python",
    version=VERSION,
    packages=find_packages(exclude=["tests"]),
    description="A Luno API client for Python",
    author="Neil Garb",
    author_email="neil@luno.com",
    install_requires=["requests>=2.18.4", "six>=1.11.0"],
    license="MIT",
    url="https://github.com/luno/luno-python",
    download_url=f"https://github.com/luno/luno-python/tarball/{VERSION}",
    keywords="Luno API Bitcoin Ethereum",
    test_suite="tests",
    setup_requires=["pytest-runner"],
    extras_require={
        "test": ["pytest", "pytest-cov", "requests_mock"],
        "dev": [
            "pytest",
            "pytest-cov",
            "requests_mock",
            "pre-commit",
            "black",
            "isort",
            "flake8",
            "flake8-docstrings",
            "flake8-bugbear",
            "bandit[toml]",
        ],
    },
)
