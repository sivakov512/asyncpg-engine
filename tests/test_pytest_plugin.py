import pytest
from asyncpg import Connection

from asyncpg_engine import Engine

pytestmark = [pytest.mark.asyncio]


async def test_engine_returns_the_same_connection_by_default(db: Engine) -> None:
    async with db.acquire() as con_0:
        async with db.acquire() as con_1:

            assert con_0 == con_1


async def test_con_returns_the_same_connection_as_engine_by_default(
    db: Engine, con: Connection
) -> None:
    async with db.acquire() as con_0:

        assert con_0 == con


async def test_transactional_by_default(con: Connection) -> None:
    sql = "SELECT txid_current()"

    assert await con.fetchval(sql) == await con.fetchval(sql)


@pytest.mark.not_transactional()
async def test_engine_returns_new_connection_if_not_transactional(
    db: Engine,
) -> None:
    async with db.acquire() as con_0:
        async with db.acquire() as con_1:

            assert con_0 != con_1


@pytest.mark.not_transactional()
async def test_con_returns_not_the_same_connection_as_engine_if_not_transactional(
    db: Engine,
    con: Connection,
) -> None:
    async with db.acquire() as con_0:
        async with db.acquire() as con_1:

            assert con_0 != con_1


@pytest.mark.not_transactional()
async def test_not_in_transactional_if_marked(con: Connection) -> None:
    sql = "SELECT txid_current()"

    assert await con.fetchval(sql) != await con.fetchval(sql)
