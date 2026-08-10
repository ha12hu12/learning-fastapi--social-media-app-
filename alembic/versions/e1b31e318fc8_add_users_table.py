"""add users table

Revision ID: e1b31e318fc8
Revises: 9b2835c16579
Create Date: 2026-08-08 12:13:35.434356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1b31e318fc8'
down_revision: Union[str, Sequence[str], None] = '9b2835c16579'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("email", sa.Integer, unique=True, nullable=False),
                    sa.Column("password", sa.Integer, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP, nullable=False))

def downgrade() -> None:
    op.drop_table("users")
    pass
