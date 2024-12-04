__all__ = (
    'BaseDBEngineError',
    'UnknownDBEngineError',
    'InitDBEngineError',
    'DBOperationError',
    'DBOperationWarning',
)


class BaseDBEngineError(Exception):
    """BaseDBEngineError"""


class InitDBEngineError(BaseDBEngineError):
    """InitDBEngineError"""


class UnknownDBEngineError(BaseDBEngineError):
    """UnknownDBEngineError"""


class DBOperationError(BaseDBEngineError):
    """DBOperationError"""


class DBOperationWarning(BaseDBEngineError):
    """DBOperationWarning"""
