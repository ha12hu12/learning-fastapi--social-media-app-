"""add server default to created_at

Revision ID: 711723dcdbb8
Revises: 5827cf27b3d4
Create Date: 2026-08-13 12:16:09.935229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '711723dcdbb8'
down_revision: Union[str, Sequence[str], None] = '5827cf27b3d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users", "created_at", server_default=sa.text("now()"))



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'created_at', server_default=None)

