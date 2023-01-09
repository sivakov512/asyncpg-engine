# asyncpg-engine

Small wrapper around [asyncpg](https://github.com/MagicStack/asyncpg) for specific experience and transactional testing.

[![test Status](https://github.com/sivakov512/asyncpg-engine/actions/workflows/test.yml/badge.svg)](https://github.com/sivakov512/asyncpg-engine/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/sivakov512/asyncpg-engine/badge.svg?branch=master)](https://coveralls.io/github/sivakov512/asyncpg-engine?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Python versions](https://img.shields.io/pypi/pyversions/asyncpg-engine.svg)](https://pypi.python.org/pypi/asyncpg-engine)
[![PyPi](https://img.shields.io/pypi/v/asyncpg-engine.svg)](https://pypi.python.org/pypi/asyncpg-engine)

## Basic usage

```python
from asyncpg_engine import Engine


engine = await Engine.create("postgres://guest:guest@localhost:5432/guest?sslmode=disable")

async with engine.acquire() as con:
    # https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.connection.Connection
    assert await con.fetchval("SELECT 1") == 1
```

### Custom type conversions

You can specify [custom encoder/decoder](https://magicstack.github.io/asyncpg/current/usage.html#custom-type-conversions) by subclassing `Engine`:
```python
from asyncpg_engine import Engine
import orjson


class MyEngine(Engine):

    @staticmethod
    async def _set_codecs(con: Connection) -> None:
        # https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.connection.Connection.set_type_codec
        await con.set_type_codec(
            "json", encoder=orjson.dumps, decoder=orjson.loads, schema="pg_catalog"
        )
```

## Pytest plugin

Library includes pytest plugin with support for transactional testing.

To start using it install `pytest`, enable plugin in your root `conftest.py` and define `postgres_url` fixture that returns database connection string:
```python
pytest_plugins = ["asyncpg_engine"]


@pytest.fixture()
def postgres_url() -> str:
    return "postgres://guest:guest@localhost:5432/guest?sslmode=disable"
```

Now you can use two fixtures:

* `db` that returns `Engine` instance:
```python
async def test_returns_true(db):
    async with db.acquire() as con:
        assert await con.fetchval("SELECT true")
```

* `con` that returns already acquired connection:
```python
async def test_returns_true(con):
    assert await con.fetchval("SELECT true")
```

By default `Engine` is configured for transactional testing, so every call to `db.acquire` or `con` usage will return the same connection with already started transaction. Transaction is rolled back at the end of test, so all your changes in db are rolled back too.

You can override this behaviour with `asyncpg_engine` mark:
```python
@pytest.mark.asyncpg_engine(transactional=False)
async def test_returns_true(con):
    assert await con.fetchval("SELECT true")


@pytest.mark.asyncpg_engine(transactional=False)
async def test_returns_true_too(db):
    async with db.acquire() as con:
        assert await con.fetchval("SELECT true")
```

If you want to use your own custom `Engine` subclass in tests you can define `asyncpg_engine_cls` fixture that returns it:
```python
from asyncpg_engine import Engine


class MyPrettyEngine(Engine):
    pass


@pytest.fixture()
def asyncpg_engine_cls() -> typing.Type[MyPrettyEngine]:
    return MyPrettyEngine


async def test_returns_my_pretty_engine(db: MyPrettyEngine) -> None:
    assert isinstance(db, MyPrettyEngine)
```

## Development and contribution

First of all you should install [Poetry](https://python-poetry.org).

* install project dependencies
```bash
make install
```

* run linters
```bash
make lint
```

* run tests
```bash
make test
```

* feel free to contribute!
