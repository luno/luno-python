from setuptools import setup, find_packages

from luno_python import VERSION

setup(
    name='luno-python',
    version=VERSION,
    packages=find_packages(exclude=['tests']),
    description='A Luno API client for Python',
    author='Neil Garb',
    author_email='neil@luno.com',
    install_requires=['requests>=2.18.4', 'six>=1.11.0'],
    license='MIT',
    url='https://github.com/luno/luno-python',
    download_url='https://github.com/luno/luno-python/tarball/%s' % (VERSION, ),
    keywords='Luno API Bitcoin Ethereum',
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'requests_mock']
)

