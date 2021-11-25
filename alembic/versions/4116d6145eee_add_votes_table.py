"""add votes table

Revision ID: 4116d6145eee
Revises: f2ab352b519f
Create Date: 2021-11-25 20:16:24.002921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4116d6145eee'
down_revision = 'f2ab352b519f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    )


def downgrade():
    op.drop_table("votes")
