import logging.config

from logging import Logger
from typing import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn

# from alembic import command
# from alembic.config import Config
from fastapi import FastAPI

from app.manager import TaskManager
from app.config import CONFIGURATION
from app.api.http.handler.task import TaskHandler
from app.dao.sqlalchemy.db_engine import SQLAlchemyDBEngine
from app.dao.sqlalchemy.model.task import SQLAlchemyTaskDAO


__all__ = (
    'start_app',
)

LOG: Logger


# @asynccontextmanager
# async def __run_migrations() -> AsyncIterator[None]:
#     alembic_cfg = Config("alembic.ini")
#
#     try:
#         command.upgrade(alembic_cfg, "head")
#
#         yield
#
#     except (Exception,) as error:
#         LOG.error(f"An error occurred during migration: {error}")
#
#     finally:
#         pass

def __configure_logger() -> None:
    """Configure the logger."""

    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

    global LOG
    LOG = logging.getLogger(__name__)


def __create_db_engine() -> SQLAlchemyDBEngine:
    """__create_db_engine.

    :returns SQLAlchemyDBEngine:
    :raises AttributeError: ?
    """

    db_engine = SQLAlchemyDBEngine(
        db_url_template=CONFIGURATION.DB_SETTINGS.DATABASE_URL_TEMPLATE,
        username=CONFIGURATION.DB_SETTINGS.DB_USERNAME,
        password=CONFIGURATION.DB_SETTINGS.DB_PASSWORD,
        host=CONFIGURATION.DB_SETTINGS.DB_HOST,
        port=CONFIGURATION.DB_SETTINGS.DB_PORT,
        database=CONFIGURATION.DB_SETTINGS.DB_DATABASE,
    )

    return db_engine


@asynccontextmanager
async def __lifespan(app: FastAPI) -> AsyncIterator[None]:
    LOG.info("startup")

    # LOG.info("Running migrations...")
    # __run_migrations()

    LOG.info("Starting db_engine...")

    db_engine = __create_db_engine()

    LOG.info("Initializing task layers...")

    task_dao = SQLAlchemyTaskDAO(db_engine=db_engine)
    task_manager = TaskManager(task_dao=task_dao)
    task_handler = TaskHandler(task_manager=task_manager)

    LOG.info("Adding task routes...")

    app.include_router(task_handler.router, prefix="/tasks")
    yield

    LOG.info("Shutting down...")


def start_app() -> None:
    __configure_logger()

    LOG.info("Starting fastapi app instance...")
    app = FastAPI(lifespan=__lifespan)

    LOG.info("Running uvicorn server...")
    uvicorn.run(
        app,
        host=CONFIGURATION.APP_SETTINGS.APP_HOST,
        port=CONFIGURATION.APP_SETTINGS.APP_PORT,
    )
