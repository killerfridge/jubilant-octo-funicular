"""add additional columns to the post model

Revision ID: f2ab352b519f
Revises: 88fb6b937217
Create Date: 2021-11-25 16:47:30.008058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2ab352b519f'
down_revision = '88fb6b937217'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column("is_published", sa.Boolean, nullable=False, server_default="TRUE"))
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))


def downgrade():
    op.drop_column("posts", "is_published")
    op.drop_column("posts", "created_at")
