"""add content column to posts table

Revision ID: 9408f9a51fa8
Revises: a6277717a913
Create Date: 2024-01-21 09:57:27.277700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9408f9a51fa8'
down_revision: Union[str, None] = 'a6277717a913'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
