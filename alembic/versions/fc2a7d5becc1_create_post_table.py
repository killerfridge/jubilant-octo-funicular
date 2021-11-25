"""create post table

Revision ID: fc2a7d5becc1
Revises: 
Create Date: 2021-11-25 16:13:15.510122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc2a7d5becc1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table('posts')
