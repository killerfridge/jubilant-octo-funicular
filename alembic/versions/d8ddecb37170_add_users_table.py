"""add users table

Revision ID: d8ddecb37170
Revises: 693d3fda2f73
Create Date: 2021-11-25 16:27:51.765227

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text


# revision identifiers, used by Alembic.
revision = 'd8ddecb37170'
down_revision = '693d3fda2f73'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        Column("id", Integer, primary_key=True, nullable=False),
        Column("email", String, nullable=False, unique=True),
        Column("password", String, nullable=False),
        Column("username", String, nullable=False, unique=True),
        Column("created_at", TIMESTAMP(timezone=True), nullable=False,
               server_default=text("now()"))
    )


def downgrade():
    op.drop_table("users")
