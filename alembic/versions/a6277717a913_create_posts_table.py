"""create posts table

Revision ID: a6277717a913
Revises: 
Create Date: 2024-01-17 09:20:27.302700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6277717a913'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_table('posts')
    pass
