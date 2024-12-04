__all__ = (
    'BaseManagerError',
    'DAOManagerError',
    'DataManagerError',
)


class BaseManagerError(Exception):
    """BaseDBEngineError"""


class DAOManagerError(BaseManagerError):
    """DAOManagerError"""


class DataManagerError(BaseManagerError):
    """DataManagerError"""
