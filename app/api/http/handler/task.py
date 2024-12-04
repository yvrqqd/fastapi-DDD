import logging

from typing import List

from fastapi import APIRouter, HTTPException, Depends

from app.manager.exceptions import DAOManagerError, DataManagerError
from app.api.http.exceptions import BaseAPIError
from app.dto.task import *
from app.manager import TaskManager


__all__ = (
    'TaskHandler',
)

LOG = logging.getLogger(__name__)


class TaskHandler:
    """Task handler."""

    __slots__ = (
        '__task_manager',
        'router',
    )

    def __init__(self, task_manager: TaskManager) -> None:
        """Initialization.

        :param task_manager:
        :raises BaseAPIError:
        """

        self.__task_manager = task_manager

        self.router = APIRouter()
        self.__add_routes()

    def __add_routes(self) -> None:
        """__add_routes.

        :raises BaseAPIError:
        """

        try:
            self.router.add_api_route(
                "/",
                self.create,
                methods=["POST"],
                response_model=CreateTaskResponse,
                tags=["Task"],
            )
            self.router.add_api_route(
                "/{task_id}",
                self.get,
                methods=["GET"],
                response_model=ReadTaskResponse | None,
                tags=["Task"],
            )
            self.router.add_api_route(
                "/",
                self.get_list,
                methods=["GET"],
                response_model=List[ReadTaskResponse],
                tags=["Task"],
            )
            self.router.add_api_route(
                "/{task_id}",
                self.update,
                methods=["PUT"],
                response_model=UpdateTaskResponse,
                tags=["Task"],
            )
            self.router.add_api_route(
                "/{task_id}",
                self.delete,
                methods=["DELETE"],
                response_model=DeleteTaskResponse,
                tags=["Task"],
            )

        except (Exception,) as error:
            LOG.error(f"Unknown error during adding task routes. err={error}")

            raise BaseAPIError from error


    async def get_list(self, filter_parameters: ReadTaskListRequest = Depends()) -> List[ReadTaskResponse]:
        """This method lets you get list of tasks with optional filtering by status"""

        LOG.info(f"Handled get_list request: filter_parameters={filter_parameters}")

        try:
            found_tasks = await self.__task_manager.get_task_list(filter_parameters)

        except DAOManagerError:
            raise HTTPException(status_code=500, detail="Internal error")

        except DataManagerError:
            raise HTTPException(status_code=404, detail="Incorrect data")

        return found_tasks

    async def get(self, task_id: int) -> ReadTaskResponse | None:
        """This method lets you get task by id"""

        LOG.info(f"Handled get request: task_id={task_id}")

        try:
            found_task = await self.__task_manager.get_task(task_id)

        except DAOManagerError:
            raise HTTPException(status_code=500, detail="Internal error")

        except DataManagerError:
            raise HTTPException(status_code=404, detail="Incorrect data")

        return found_task

    async def create(self, task: CreateTaskRequest = Depends()) -> CreateTaskResponse:
        """This method lets you create a new task"""

        LOG.info(f"Handled create request: task={task}")

        try:
            created_task = await self.__task_manager.create_task(task)

        except DAOManagerError:
            raise HTTPException(status_code=500, detail="Internal error")

        except DataManagerError:
            raise HTTPException(status_code=404, detail="Incorrect data")

        return created_task

    async def update(self, task_id: int, task: UpdateTaskRequest = Depends()) -> UpdateTaskResponse:
        """This method lets you update an existing task that would be found by id"""

        LOG.info(f"Handled update request: task_id={task_id}, task={task}")

        try:
            updated_task = await self.__task_manager.update_task(task_id, task)

        except DAOManagerError:
            raise HTTPException(status_code=500, detail="Internal error")

        except DataManagerError:
            raise HTTPException(status_code=404, detail="Incorrect data")

        return updated_task

    async def delete(self, task_id: int) -> DeleteTaskResponse:
        """This method lets you delete an existing task that would be found by id"""

        LOG.info(f"Handled delete request: task_id={task_id}")

        try:
            deleted_task = await self.__task_manager.delete_task(task_id)

        except DAOManagerError:
            raise HTTPException(status_code=500, detail="Internal error")

        except DataManagerError:
            raise HTTPException(status_code=404, detail="Incorrect data")

        return deleted_task
