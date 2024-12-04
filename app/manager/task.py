import logging

from typing import List

from app.dto.task import *
from app.dao.sqlalchemy.model.task import SQLAlchemyTaskDAO
from app.manager.exceptions import DataManagerError, DAOManagerError
from app.dao.sqlalchemy.exceptions import DBOperationError, DBOperationWarning


__all__ = (
    'TaskManager',
)

LOG = logging.getLogger(__name__)


class TaskManager:
    """Task manager."""

    __slots__ = (
        '__task_dao',
    )

    def __init__(self, task_dao: SQLAlchemyTaskDAO) -> None:
        """Initialization.

        :param task_dao:
        """

        self.__task_dao = task_dao

    async def create_task(self, task: CreateTaskRequest) -> CreateTaskResponse:
        """create_task.

        :raises DAOManagerError:
        :raises DataManagerError:
        """

        LOG.info(f"Manager create request: task={task}")

        try:
            created_task = await self.__task_dao.create(task)

        except DBOperationError as error:
            raise DAOManagerError from error

        except DBOperationWarning as error:
            raise DataManagerError from error

        return created_task

    async def get_task(self, task_id: int) -> ReadTaskResponse | None:
        """get_task.

        :raises DAOManagerError:
        :raises DataManagerError:
        """

        LOG.info(f"Manager get request: task_id={task_id}")

        try:
            found_task = await self.__task_dao.get(task_id)

        except DBOperationError as error:
            raise DAOManagerError from error

        except DBOperationWarning as error:
            raise DataManagerError from error

        return found_task

    async def get_task_list(self, filter_parameters: ReadTaskListRequest) -> List[ReadTaskResponse]:
        """get_task_list.

        :raises DAOManagerError:
        :raises DataManagerError:
        """

        LOG.info(f"Manager get_list request: filter_parameters={filter_parameters}")

        try:
            found_tasks = await self.__task_dao.get_list(filter_parameters)

        except DBOperationError as error:
            raise DAOManagerError from error

        except DBOperationWarning as error:
            raise DataManagerError from error

        return found_tasks

    async def update_task(self, task_id: int, task: UpdateTaskRequest) -> UpdateTaskResponse:
        """update_task.

        :raises DAOManagerError:
        :raises DataManagerError:
        """

        LOG.info(f"Manager update request: task_id={task_id}, task={task}")

        try:
            updated_task = await self.__task_dao.update(task_id, task)

        except DBOperationError as error:
            raise DAOManagerError from error

        except DBOperationWarning as error:
            raise DataManagerError from error

        return updated_task

    async def delete_task(self, task_id: int) -> DeleteTaskResponse:
        """delete_task.

        :raises DAOManagerError:
        :raises DataManagerError:
        """

        LOG.info(f"Manager delete request: task_id={task_id}")

        try:
            deleted_task = await self.__task_dao.delete(task_id)

        except DBOperationError as error:
            raise DataManagerError from error

        except DBOperationWarning as error:
            raise DataManagerError from error

        return deleted_task

