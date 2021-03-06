"""shouts-fixtures-relationships

Revision ID: bf826fdd86b7
Revises: 1fe1bfa4b0bb
Create Date: 2021-07-01 16:18:34.876730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf826fdd86b7'
down_revision = '1fe1bfa4b0bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commenters',
    sa.Column('shout_id', sa.Integer(), nullable=True),
    sa.Column('fixture_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fixture_id'], ['fixtures.id'], ),
    sa.ForeignKeyConstraint(['shout_id'], ['shouts.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commenters')
    # ### end Alembic commands ###
