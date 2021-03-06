"""Added initial table

Revision ID: 1d9e718e1c9b
Revises: None
Create Date: 2014-08-23 14:49:14.351909

"""

# revision identifiers, used by Alembic.
revision = '1d9e718e1c9b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock',
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('location', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['symbol'], ['stock.symbol'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('history')
    op.drop_table('stock')
    ### end Alembic commands ###
