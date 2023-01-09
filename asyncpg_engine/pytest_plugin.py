import typing

import pytest
import pytest_asyncio
from asyncpg import Connection

from asyncpg_engine import Engine


def pytest_configure(config: typing.Any) -> None:
    config.addinivalue_line("markers", "asyncpg_engine: configure asyncpg-engine plugin behaviour.")


@pytest.fixture()
def asyncpg_engine_cls() -> typing.Type[Engine]:
    return Engine


@pytest_asyncio.fixture()
async def db(
    request: pytest.FixtureRequest, asyncpg_engine_cls: typing.Type[Engine], postgres_url: str
) -> typing.AsyncGenerator[Engine, None]:
    plugin_config = request.node.get_closest_marker("asyncpg_engine")

    transactional = getattr(plugin_config, "kwargs", {}).get("transactional", True)

    _db = await asyncpg_engine_cls.create(url=postgres_url, use_single_connection=transactional)

    con: Connection = await _db.acquire()  # type: ignore
    tr = con.transaction()
    await tr.start()

    yield _db

    await tr.rollback()
    await _db.release(con, force=transactional)
    await _db.close()


@pytest_asyncio.fixture()
async def con(db: Engine) -> typing.AsyncGenerator[Connection, None]:
    async with db.acquire() as _con:
        yield _con
