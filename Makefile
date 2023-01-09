install:
	poetry install

install-no-dev:
	poetry install --no-dev

lint:
	poetry run flake8
	poetry run mypy ./

test:
	poetry run pytest

test-with-coverage:
	poetry run pytest --cov=asyncpg_engine

upload-coverage:
	poetry run coveralls
