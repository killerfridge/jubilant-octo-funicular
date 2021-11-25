"""empty message

Revision ID: 693d3fda2f73
Revises: fc2a7d5becc1
Create Date: 2021-11-25 16:22:20.858310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '693d3fda2f73'
down_revision = 'fc2a7d5becc1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )


def downgrade():
    op.drop_column(
        "posts", "content"
    )
