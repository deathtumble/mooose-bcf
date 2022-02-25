PYTHON_VERSION ?= 3.8.12
PIP ?= pip3
POETRY ?= poetry $(POETRY_OPTS)
ACTIVATE ?= . .venv/bin/activate

GIT_REF ?= refs/heads/$(shell git rev-parse --abbrev-ref HEAD)
GIT_SHA ?= $(shell git rev-parse HEAD)
SHA1_START := $(shell echo ${GIT_SHA} | cut -c -2)
SHA1_END := $(shell echo ${GIT_SHA} | cut -c 3-)
GIT_DIRTY ?= $(if $(shell git diff --stat),true,false)
GIT_REF_TYPE ?= branch

.PHONY: unittest 

.venv/bin/python:
	python3 -m venv .venv
	. .venv/bin/activate
	python3 -m pip3 install --upgrade pip
	python3 -m pip3 install poetry

poetry-lock.json:

pyproject.toml:

poetry.toml:

.venv/lib: poetry.lock pyproject.toml poetry.toml
	poetry install

.venv: .venv/bin/python .venv/lib

unittest:
	${ACTIVATE} && GIT_REF=${GIT_REF} ${POETRY} run pytest --junitxml=./build/test-reports/unittest.xml --html=./build/test-reports/html/unittest.html