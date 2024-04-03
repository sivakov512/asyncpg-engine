import pytest

pytest_plugins = ["asyncpg_engine"]


@pytest.fixture
def postgres_url() -> str:
    return "postgres://guest:guest@localhost:5432/guest?sslmode=disable"
