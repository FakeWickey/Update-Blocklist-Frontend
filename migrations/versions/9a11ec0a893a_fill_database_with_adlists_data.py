"""Fill database with adlists data

Revision ID: 9a11ec0a893a
Revises: fd249bdfa7a5
Create Date: 2022-12-22 21:06:41.030798

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import mysql

from sqlalchemy import insert, table, column, String


# revision identifiers, used by Alembic.
revision = '9a11ec0a893a'
down_revision = 'fd249bdfa7a5'
branch_labels = None
depends_on = None


def upgrade():
    # Fills the table with the default adlists data
    accounts_table = table('adlists',
        column('url', String),
        column('type', String)
    )

    op.bulk_insert(accounts_table,
        [
            {'url': 'https://someonewhocares.org/hosts/hosts', 'type': 'hosts'},
            {'url': 'https://malware-filter.pages.dev/urlhaus-filter-online.txt', 'type': 'adblock'},
            {'url': 'https://easylist.to/easylist/easyprivacy.txt', 'type': 'adblock'}
        ]
    )


def downgrade():
    # Empty the table
    op.execute("TRUNCATE TABLE adlists")
