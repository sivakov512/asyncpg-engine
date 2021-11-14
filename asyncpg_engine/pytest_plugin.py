import typing as t

import pytest
from asyncpg import Connection

from asyncpg_engine import Engine


def pytest_configure(config: t.Any) -> None:
    config.addinivalue_line(
        "markers", "asyncpg_engine: configure asyncpg-engine plugin behaviour."
    )


@pytest.fixture()
async def db(
    request: pytest.FixtureRequest, postgres_url: str
) -> t.AsyncGenerator[Engine, None]:
    plugin_config = request.node.get_closest_marker("asyncpg_engine")

    transactional = getattr(plugin_config, "kwargs", {}).get("transactional", True)

    _db = await Engine.create(url=postgres_url, use_single_connection=transactional)

    con: Connection = await _db.acquire()
    tr = con.transaction()
    await tr.start()

    yield _db

    await tr.rollback()
    await _db.release(con, force=transactional)
    await _db.close()


@pytest.fixture()
async def con(db: Engine) -> t.AsyncGenerator[Connection, None]:
    async with db.acquire() as _con:
        yield _con
