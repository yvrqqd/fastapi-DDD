from pydantic_settings import BaseSettings


__all__ = (
    'CONFIGURATION',
)


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: str = 'DEBUG'


class AppSettings(BaseSettings):
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000


class DBSettings(BaseSettings):
    DB_DRIVER: str = 'asyncpg'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USERNAME: str = 'db_tmp'
    DB_PASSWORD: str = 'db_tmp'
    DB_DATABASE: str = 'db_tmp'
    DB_SCHEMA: str = 'todo_list'
    DATABASE_URL_TEMPLATE: str = 'postgresql+asyncpg://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s'


class Configuration(BaseSettings):
    LOGGING_SETTINGS: LoggingSettings = LoggingSettings()
    DB_SETTINGS: DBSettings = DBSettings()
    APP_SETTINGS: AppSettings = AppSettings()


CONFIGURATION: Configuration = Configuration()
