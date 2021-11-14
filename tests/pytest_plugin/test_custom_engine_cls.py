import typing as t

import pytest

from asyncpg_engine import Engine

pytestmark = [pytest.mark.asyncio]


class MyPrettyEngine(Engine):
    pass


@pytest.fixture()
def asyncpg_engine_cls() -> t.Type[MyPrettyEngine]:
    return MyPrettyEngine


async def test_returns_my_pretty_engine(db: MyPrettyEngine) -> None:
    assert isinstance(db, MyPrettyEngine)
