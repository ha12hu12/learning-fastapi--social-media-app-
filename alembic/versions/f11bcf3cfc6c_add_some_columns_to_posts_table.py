"""add some columns to posts table

Revision ID: f11bcf3cfc6c
Revises: 771dd0140a60
Create Date: 2026-08-08 14:29:37.144393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f11bcf3cfc6c'
down_revision: Union[str, Sequence[str], None] = '771dd0140a60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                   sa.Column("published",sa.Boolean, nullable=False, 
                             server_default='TRUE'))
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                             server_default=sa.text("now()")) )


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
