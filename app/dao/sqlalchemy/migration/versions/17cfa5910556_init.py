"""init

Revision ID: 17cfa5910556
Revises: 
Create Date: 2024-12-01 22:48:01.587902

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

from app.dto.task import TaskStatus


# revision identifiers, used by Alembic.
revision: str = '17cfa5910556'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), default=''),
        sa.Column('status', sa.Enum(TaskStatus), nullable=False, default=TaskStatus.TODO),
        schema='todo_list'
    )


def downgrade() -> None:
    op.drop_table('task', schema='todo_list')
