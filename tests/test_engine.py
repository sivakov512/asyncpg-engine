import pytest
import pytest_asyncio
from asyncpg import InterfaceError

from asyncpg_engine import Engine

pytestmark = [pytest.mark.asyncio]


@pytest_asyncio.fixture()
async def engine(postgres_url: str) -> Engine:
    return await Engine.create(postgres_url)


async def test_returns_new_connection_every_acquire(engine: Engine) -> None:
    async with engine.acquire() as con_0:
        async with engine.acquire() as con_1:

            assert con_0 != con_1


async def test_returns_the_same_connection_every_acquire_if_single(postgres_url: str) -> None:
    engine = await Engine.create(postgres_url, use_single_connection=True)

    async with engine.acquire() as con_0:
        async with engine.acquire() as con_1:

            assert con_0 == con_1


async def test_non_force_release_ignored_for_single_connection(postgres_url: str) -> None:
    engine = await Engine.create(postgres_url, use_single_connection=True)
    async with engine.acquire() as con_0:
        pass
    async with engine.acquire() as con_1:

        assert con_0 is con_1

    await engine.release(con_0, force=True)
    await engine.release(con_1, force=True)


async def test_closes_well(engine: Engine) -> None:
    await engine.close()

    with pytest.raises(InterfaceError):
        await engine.acquire()


async def test_healthcheck_returns_nothing(engine: Engine) -> None:
    got = await engine.healthcheck()

    assert got is None


async def test_healthcheck_raises_if_something_went_wrong(engine: Engine) -> None:
    await engine.close()

    with pytest.raises(InterfaceError):
        await engine.healthcheck()
