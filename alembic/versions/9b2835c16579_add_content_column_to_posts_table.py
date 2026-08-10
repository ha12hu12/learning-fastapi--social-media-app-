"""add content column to posts table

Revision ID: 9b2835c16579
Revises: 527cdaf658f6
Create Date: 2026-08-08 12:04:14.356754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b2835c16579'
down_revision: Union[str, Sequence[str], None] = '527cdaf658f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
                  sa.Column("content",sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
