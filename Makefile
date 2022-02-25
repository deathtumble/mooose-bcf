PYTHON_VERSION ?= 3.8.12
PIP ?= pip3
POETRY ?= poetry $(POETRY_OPTS)

.venv/bin/python:
	python3 -m venv .venv
	. .venv/bin/activate
	python3 -m pip install --upgrade pip
	python3 -m pip install poetry


.venv/lib: poetry.lock pyproject.toml poetry.toml
	poetry install

.venv: .venv/bin/python .venv/lib

