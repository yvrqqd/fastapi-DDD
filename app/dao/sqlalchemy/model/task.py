import logging

from typing import List

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    select,
    update,
    delete,
    insert,
)
from sqlalchemy.exc import SQLAlchemyError

from app.dto.task import *
from app.config import CONFIGURATION
from app.dao.sqlalchemy.exceptions import (
    BaseDBEngineError,
    DBOperationError,
    DBOperationWarning,
    UnknownDBEngineError,
)
from app.dao.sqlalchemy.db_engine import SQLAlchemyDBEngine
from app.dao.sqlalchemy.model.base import Base


__all__ = (
    'SQLAlchemyTaskDAO',
)

LOG = logging.getLogger(__name__)


class SQLAlchemyTaskModel(Base):
    __tablename__ = 'task'
    __table_args__ = {
        'schema': CONFIGURATION.DB_SETTINGS.DB_SCHEMA,
    }

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(String(), default='')
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)


class SQLAlchemyTaskDAO:
    """SQLAlchemyTaskDAO"""

    __slots__ = (
        '__db_engine',
    )

    def __init__(self, db_engine: SQLAlchemyDBEngine) -> None:
        """Initialization.

        :param db_engine: SQLAlchemyDBEngine.
        """

        self.__db_engine = db_engine

    async def get(self, task_id: int) -> ReadTaskResponse | None:
        """Gets task.

        :param task_id:
        :returns: TaskDTO if found, else None.
        :raises DBOperationError: When error is in engine.
        :raises DBOperationWarning: When error is in data.
        """

        LOG.info(f"DAO get request: task_id={task_id}")

        try:
            query = select(SQLAlchemyTaskModel).where(SQLAlchemyTaskModel.id == task_id)

            async with self.__db_engine.acquire_connection as conn:
                task_raw = (await conn.execute(query)).mappings().first()

            found_task = ReadTaskResponse(**task_raw) if task_raw else None

        except (
                SQLAlchemyError,
                BaseDBEngineError,
                UnknownDBEngineError,
        ) as error:
            LOG.error(f"DAO err: {error}")

            raise DBOperationError from error

        except (
                AttributeError,
                TypeError,
        ) as warning:
            LOG.warning(f"DAO warning: {warning}")

            raise DBOperationWarning from warning

        return found_task


    async def get_list(self, filter_parameters: ReadTaskListRequest) -> List[ReadTaskResponse]:
        """Gets task list.

        :param filter_parameters: TaskDTO.
        :returns: TaskDTO of create task.
        :raises DBOperationError: When error is in engine.
        :raises DBOperationWarning: When error is in data.
        """

        LOG.info(f"DAO get_list request: filter_parameters={filter_parameters}")

        try:
            query = select(SQLAlchemyTaskModel)

            if filter_parameters.status:
                query = query.where(SQLAlchemyTaskModel.status == filter_parameters.status)

            async with self.__db_engine.acquire_connection as conn:
                task_list_raw = (await conn.execute(query)).mappings().all()

            found_task_list = [ReadTaskResponse(**row) for row in task_list_raw]

        except (
                SQLAlchemyError,
                BaseDBEngineError,
                UnknownDBEngineError,
        ) as error:
            LOG.error(f"DAO err: {error}")

            raise DBOperationError from error

        except (
                AttributeError,
                TypeError,
        ) as warning:
            LOG.warning(f"DAO warning: {warning}")

            raise DBOperationWarning from warning

        return found_task_list

    async def create(self, task: CreateTaskRequest) -> CreateTaskResponse:
        """Creates task.

        :param task: TaskDTO.
        :returns: TaskDTO of create task.
        :raises DBOperationError: When error is in engine.
        :raises DBOperationWarning: When error is in data.
        """

        LOG.info(f"DAO create request: task={task}")

        try:
            query = insert(
                SQLAlchemyTaskModel
            ).values(
                **task.model_dump(),
            ).returning(
                SQLAlchemyTaskModel
            )

            async with self.__db_engine.acquire_connection as conn:
                task_raw = (await conn.execute(query)).mappings().first()

                await conn.commit()

            created_task = CreateTaskResponse(**task_raw)

        except (
                SQLAlchemyError,
                BaseDBEngineError,
                UnknownDBEngineError,
        ) as error:
            LOG.error(f"DAO err: {error}")

            raise DBOperationError from error

        except (
                AttributeError,
                TypeError,
        ) as warning:
            LOG.warning(f"DAO warning: {warning}")

            raise DBOperationWarning from warning

        return created_task

    async def update(self, task_id: int, task: UpdateTaskRequest) -> UpdateTaskResponse:
        """Updates task.

        :param task_id: Task id.
        :param task: TaskDTO.
        :returns: TaskDTO of updated task.
        :raises DBOperationError: When error is in engine.
        :raises DBOperationWarning: When error is in data.
        """

        LOG.info(f"DAO update request: task_id={task_id}, task={task}")

        try:
            query = update(
                SQLAlchemyTaskModel
            ).where(
                SQLAlchemyTaskModel.id == task_id
            ).values(
                **task.model_dump(),
            ).returning(
                SQLAlchemyTaskModel
            )

            async with self.__db_engine.acquire_connection as conn:
                updated_task_raw = (await conn.execute(query)).mappings().first()

                await conn.commit()

            updated_task = UpdateTaskResponse(**updated_task_raw)

        except (
                SQLAlchemyError,
                BaseDBEngineError,
                UnknownDBEngineError,
        ) as error:
            LOG.error(f"DAO err: {error}")

            raise DBOperationError from error

        except (
                AttributeError,
                TypeError,
        ) as warning:
            LOG.warning(f"DAO warning: {warning}")

            raise DBOperationWarning from warning

        return updated_task

    async def delete(self, task_id: int) -> DeleteTaskResponse:
        """Deletes task.

        :param task_id: Task id.
        :returns: TaskDTO of deleted task.
        :raises DBOperationError: When error is in engine.
        :raises DBOperationWarning: When error is in data.
        """

        LOG.info(f"DAO delete request: task_id={task_id}")

        try:
            query = delete(
                SQLAlchemyTaskModel
            ).where(
                SQLAlchemyTaskModel.id == task_id
            ).returning(
                SQLAlchemyTaskModel
            )

            async with self.__db_engine.acquire_connection as conn:
                deleted_task_raw = (await conn.execute(query)).mappings().first()

                await conn.commit()

            deleted_task = DeleteTaskResponse(**deleted_task_raw)

        except (
                SQLAlchemyError,
                BaseDBEngineError,
                UnknownDBEngineError,
        ) as error:
            LOG.error(f"DAO err: {error}")

            raise DBOperationError from error

        except (
                AttributeError,
                TypeError,
        ) as warning:
            LOG.warning(f"DAO warning: {warning}")

            raise DBOperationWarning from warning

        return deleted_task
