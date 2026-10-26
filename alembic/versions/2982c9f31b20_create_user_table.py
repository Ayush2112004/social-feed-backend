"""create user table

Revision ID: 2982c9f31b20
Revises: 2fab6e93b616
Create Date: 2026-10-26 01:14:21.601929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2982c9f31b20'
down_revision: Union[str, Sequence[str], None] = '2fab6e93b616'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",sa.Column("id",sa.Integer(),primary_key=True,nullable=False),sa.Column("email",sa.String(),nullable=False,unique=True),sa.Column("password",sa.String(),nullable=False),sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.func.now()))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
