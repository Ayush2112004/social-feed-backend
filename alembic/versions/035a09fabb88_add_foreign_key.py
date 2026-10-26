"""add foreign key

Revision ID: 035a09fabb88
Revises: 2982c9f31b20
Create Date: 2026-10-26 14:49:13.866763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '035a09fabb88'
down_revision: Union[str, Sequence[str], None] = '2982c9f31b20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name="posts")
    op.drop_column("posts","owner_id")