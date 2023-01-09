__all__ = ["Engine"]

import typing
from types import TracebackType

from asyncpg import Connection, create_pool
from asyncpg.pool import Pool


class Engine:
    __slots__ = "_pool", "_use_single_con", "_global_con"

    _pool: Pool
    _use_single_con: bool
    _global_con: typing.Optional[Connection]

    def __init__(self, pool: Pool, use_single_connection: bool):
        self._pool = pool
        self._use_single_con = use_single_connection

        self._global_con = None

    @classmethod
    async def create(
        cls, url: str, *, use_single_connection: bool = False, **kwargs: typing.Any
    ) -> "Engine":
        pool = await create_pool(url, min_size=2, init=cls._set_codecs, **kwargs)
        return cls(pool, use_single_connection)

    async def close(self) -> None:
        await self._pool.close()

    def acquire(self) -> "ConnectionAcquire":
        return ConnectionAcquire(self)

    async def _acquire(self) -> Connection:
        if self._use_single_con:
            self._global_con = self._global_con or await self._pool.acquire()
            return self._global_con

        return await self._pool.acquire()

    async def release(self, con: Connection, *, force: bool = False) -> None:
        if not self._use_single_con or force:
            await self._pool.release(con)
            self._global_con = None

    async def healthcheck(self) -> None:
        async with self.acquire() as con:  # type: Connection
            await con.execute("SELECT 1")

    @staticmethod
    async def _set_codecs(con: Connection) -> None:
        """Override this method if you want to set custom codecs."""


class ConnectionAcquire:
    __slots__ = "engine", "con"

    engine: Engine
    con: typing.Optional[Connection]

    def __init__(self, engine: Engine):
        self.engine = engine
        self.con = None

    async def __call__(self) -> Connection:
        self.con = await self.engine._acquire()
        return self.con

    def __await__(self) -> typing.Generator[Connection, None, None]:
        return self().__await__()

    async def __aenter__(self) -> Connection:
        return await self()

    async def __aexit__(
        self, exc_type: typing.Type[BaseException], exc: BaseException, tv: TracebackType
    ) -> None:
        await self.engine.release(self.con)
