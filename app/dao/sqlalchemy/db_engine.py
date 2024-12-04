import logging

from contextlib import asynccontextmanager

from asyncpg import PostgresError
from sqlalchemy.exc import SQLAlchemyError

from app.utils.singleton import Singleton
from app.dao.sqlalchemy.exceptions import (
    BaseDBEngineError,
    UnknownDBEngineError,
    InitDBEngineError,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
)


__all__ = (
    'SQLAlchemyDBEngine',
)

LOG = logging.getLogger(__name__)


class SQLAlchemyDBEngine(metaclass=Singleton):
    """SQLAlchemyDBEngine"""

    __async_engine: AsyncEngine | None = None

    def __init__(
            self,
            db_url_template: str,
            username: str,
            password: str,
            host: str,
            port: int,
            database: str,
    ) -> None:
        """Initialize the database engine instance.

        :param db_url_template:
        :param username:
        :param password:
        :param host:
        :param port:
        :param database:
        """

        LOG.info(f"Initializing SQLAlchemyDBEngine | 'host': {host}, 'port': {port}.")

        self.__db_url: str = db_url_template % {
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
        }

    async def get_async_engine(self) -> AsyncEngine:
        """get_async_engine.

        :raises InitDBEngineError:
        """

        LOG.info(f"Trying to get AsyncEngine.")

        try:
            if self.__async_engine is None:
                self.__async_engine = await self.__create_async_engine()

        except InitDBEngineError as error:
            LOG.error(f"Failed to create or get async engine | 'err': {error}")

            raise

        return self.__async_engine

    async def __create_async_engine(self) -> AsyncEngine:
        """Creates an async SQLAlchemy engine.

        :raises InitDBEngineError:
        """

        LOG.info(f"Trying to create async engine. db_url={self.__db_url}")

        try:
            engine = create_async_engine(
                self.__db_url,
                echo=True,
            )

            LOG.info("Async engine created successfully")

            return engine

        except Exception as error:
            LOG.error(f"Failed to create async engine | 'err': {error}")

            raise InitDBEngineError from error

    @property
    @asynccontextmanager
    async def acquire_connection(self):
        """Async context manager for acquiring a connection.
        Rolls back open transactions on error.

        :raises BaseDBEngineError:
        :raises UnknownDBEngineError:
        """

        if not self.__async_engine:
            await self.get_async_engine()

        async with self.__async_engine.connect() as conn:
            try:
                yield conn

            except (
                    SQLAlchemyError,
                    PostgresError,
            ) as error:
                LOG.error(f"SQLAlchemyError on acquire_connection, 'err': {error}")

                raise BaseDBEngineError("SQLAlchemyError") from error

            except AttributeError as error:
                LOG.error(f"AttributeError on acquire_connection, 'err': {error}")

                raise BaseDBEngineError("AttributeError error") from error

            except (Exception,) as error:
                LOG.error(f"Unknown on acquire_connection, 'err': {error}")

                raise UnknownDBEngineError("Unknown error") from error

            finally:
                await conn.rollback()
