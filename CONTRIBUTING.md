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
pip install -e '.[test]'
```

## Run Tests
```bash
pytest
```