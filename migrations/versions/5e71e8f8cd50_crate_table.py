"""crate table

Revision ID: 5e71e8f8cd50
Revises: acb9b108354b
Create Date: 2020-04-07 13:10:34.488541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e71e8f8cd50'
down_revision = 'acb9b108354b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_cases', sa.Column('priority', sa.SMALLINT(), nullable=True))
    op.add_column('test_suites', sa.Column('suites_name', sa.String(length=60), nullable=False, comment='suites名称'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_suites', 'suites_name')
    op.drop_column('test_cases', 'priority')
    # ### end Alembic commands ###
