"""add foreign key to posts table

Revision ID: 88fb6b937217
Revises: d8ddecb37170
Create Date: 2021-11-25 16:35:35.553383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88fb6b937217'
down_revision = 'd8ddecb37170'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        # op.create_foreign_key("post_users_fk", source_table="posts",
        #                       referent_table="users", local_cols=['user_id'],
        #                       remote_cols=['id'], ondelete='CASCADE')
    )


def downgrade():
    op.drop_constraint("posts_user_id_fkey", "posts")
    op.drop_column(
        "posts",
        "user_id"
    )

