"""Create and define table adlists

Revision ID: fd249bdfa7a5
Revises: 
Create Date: 2022-12-18 19:09:00.734342

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fd249bdfa7a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('adlists',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('type', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('url', mysql.VARCHAR(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )




def downgrade():
    op.drop_table('adlists')
