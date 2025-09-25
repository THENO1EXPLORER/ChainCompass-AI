VENV?=.venv
PY?=python3

.PHONY: venv install format lint type test qa all

venv:
	$(PY) -m venv $(VENV)
	. $(VENV)/bin/activate; pip install -U pip

install: venv
	. $(VENV)/bin/activate; pip install -r requirements.txt
	. $(VENV)/bin/activate; pip install -r requirements-dev.txt

format:
	. $(VENV)/bin/activate; ruff check --select I --fix .
	. $(VENV)/bin/activate; black .

lint:
	. $(VENV)/bin/activate; ruff check .

type:
	. $(VENV)/bin/activate; mypy .

test:
	. $(VENV)/bin/activate; pytest

qa: format lint type test

all: install qa

