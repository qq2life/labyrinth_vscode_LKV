.PHONY: install project lint build clean fix

install:
	poetry install

project:
	poetry run python -m main

lint:
	poetry run ruff check .
	poetry run ruff format --check .

fix:
	poetry run ruff check --fix .
	poetry run ruff format .

build:
	poetry build

clean:
	rm -rf dist __pycache__ .pytest_cache .ruff_cache
