from typing import TypeVar, Generic


__all__ = (
    'Singleton',
)

T = TypeVar('T', bound='Singleton')


class Singleton(Generic[T], type):
    _instances: dict[type, T] = {}

    def __call__(cls, *args, **kwargs) -> T:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
