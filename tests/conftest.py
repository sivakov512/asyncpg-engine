import pytest

_config = {
    "POSTGRES_URL": "postgres://guest:guest@localhost:5432/guest?sslmode=disable"
}


@pytest.fixture()
def config() -> dict[str, str]:
    return _config.copy()
