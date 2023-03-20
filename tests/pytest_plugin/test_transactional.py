import pytest
from asyncpg import Connection

from asyncpg_engine import Engine

pytestmark = [pytest.mark.asyncio]


async def test_acquire_returns_the_same_connection(db: Engine) -> None:
    async with db.acquire() as con_0:
        async with db.acquire() as con_1:
            assert con_0 == con_1


async def test_con_is_the_same_as_acquire_result(db: Engine, con: Connection) -> None:
    async with db.acquire() as con_0:
        assert con_0 == con


async def test_transactional(con: Connection) -> None:
    sql = "SELECT txid_current()"

    assert await con.fetchval(sql) == await con.fetchval(sql)


@pytest.mark.asyncpg_engine(transactional=True)
async def test_transactional_if_specified(con: Connection) -> None:
    sql = "SELECT txid_current()"

    assert await con.fetchval(sql) == await con.fetchval(sql)
