import logging
import os
import sys
from logging.config import fileConfig

import sqlalchemy
from sqlalchemy import create_engine

from alembic import context

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../")
))

import app.dao.sqlalchemy.model

config = context.config

fileConfig(config.config_file_name)

target_metadata = sqlalchemy.MetaData()

LOG = logging.getLogger(__name__)

compare_type = True

def run_migrations_offline():
    LOG.error("run_migrations_offline")

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    LOG.info("run_migrations_online")

    from app.config import CONFIGURATION

    url = 'postgresql+psycopg2://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s'

    db_url = url % {
        'host': CONFIGURATION.DB_SETTINGS.DB_HOST,
        'port': CONFIGURATION.DB_SETTINGS.DB_PORT,
        'username': CONFIGURATION.DB_SETTINGS.DB_USERNAME,
        'password': CONFIGURATION.DB_SETTINGS.DB_PASSWORD,
        'database': CONFIGURATION.DB_SETTINGS.DB_DATABASE,
    }

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                LOG.info('No changes in schema.')

    def include_object(object, name, type_, reflected, compare_to):
        if type_ == "table" and reflected and compare_to is None:
            return False
        else:
            return True

    engine = create_engine(db_url)
    LOG.info('Engine created.')

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=CONFIGURATION.DB_SETTINGS.DB_SCHEMA,
            process_revision_directives=process_revision_directives,
            include_object=include_object,
            include_schemas=True
        )

        with context.begin_transaction():
            context.execute("""CREATE SCHEMA IF NOT EXISTS "%s";""" % CONFIGURATION.DB_SETTINGS.DB_SCHEMA)
            context.execute("""SET search_path TO public""")
            context.run_migrations()

    LOG.info('Migrations run.')


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
