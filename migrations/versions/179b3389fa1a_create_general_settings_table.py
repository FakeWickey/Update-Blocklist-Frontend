"""Create general settings table

Revision ID: 179b3389fa1a
Revises: 9a11ec0a893a
Create Date: 2022-12-23 23:38:46.855996

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from sqlalchemy import insert, table, column, String, Boolean

# revision identifiers, used by Alembic.
revision = '179b3389fa1a'
down_revision = '9a11ec0a893a'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('general_settings',
    sa.Column('script_enabled', mysql.BOOLEAN, nullable=False, default = True)
    )
    
    # Accounts table information
    accounts_table = table('general_settings',
        column('script_enabled', Boolean)
    )

    op.bulk_insert(accounts_table,
        [
            {'script_enabled': True}
        ]
    )


def downgrade():
    op.drop_table('general_settings')
