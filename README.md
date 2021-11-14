# asyncpg-engine

Little wrapper around [asyncpg](https://github.com/MagicStack/asyncpg) for specific experience.

[![Build Status](https://github.com/sivakov512/asyncpg-engine/actions/workflows/test.yml/badge.svg)](https://github.com/sivakov512/asyncpg-engine/actions/workflows/test.yml)
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

You can specify [custom encoder\decoder](https://magicstack.github.io/asyncpg/current/usage.html#custom-type-conversions) by subclassing `Engine`:
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

## Development and contribution

First of all you should install Poetry using [official instructions](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) or solutions provided by your distro. Then install dependencies:
```bash
poetry install
```

Run PostgreSQL using provided docker-compose configuration:
```bash
docker-compose up  # run it in another terminal or add `-d` to daemonize
```

Project uses combination of `flake8`, `black`, `isort` and `mypy` for linting and `pytest` for testing.

```bash
poetry run flake8
poetry run mypy ./
poetry run pytest
```
