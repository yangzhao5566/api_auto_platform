"""add group name

Revision ID: acb9b108354b
Revises: c70415ff93f6
Create Date: 2020-04-06 22:42:50.483751

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'acb9b108354b'
down_revision = 'c70415ff93f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('config', sa.Column('desc', sa.String(length=200), nullable=True, comment='测试组的描述'))
    op.drop_column('config', 'remark')
    op.add_column('task', sa.Column('desc', sa.String(length=200), nullable=True, comment='任务描述'))
    op.add_column('task', sa.Column('task_name', sa.String(length=80), nullable=False, comment='任务名称'))
    op.add_column('test_cases', sa.Column('desc', sa.String(length=200), nullable=True, comment='测试组的描述'))
    op.drop_column('test_cases', 'remark')
    op.add_column('test_group', sa.Column('desc', sa.String(length=200), nullable=True, comment='测试组的描述'))
    op.add_column('test_group', sa.Column('group_name', sa.String(length=200), nullable=False, comment='组名称'))
    op.drop_column('test_group', 'remark')
    op.add_column('test_suites', sa.Column('desc', sa.String(length=200), nullable=True, comment='测试组的描述'))
    op.drop_column('test_suites', 'remark')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_suites', sa.Column('remark', mysql.VARCHAR(length=200), nullable=True, comment='测试组的描述'))
    op.drop_column('test_suites', 'desc')
    op.add_column('test_group', sa.Column('remark', mysql.VARCHAR(length=200), nullable=True, comment='测试组的描述'))
    op.drop_column('test_group', 'group_name')
    op.drop_column('test_group', 'desc')
    op.add_column('test_cases', sa.Column('remark', mysql.VARCHAR(length=200), nullable=True, comment='测试组的描述'))
    op.drop_column('test_cases', 'desc')
    op.drop_column('task', 'task_name')
    op.drop_column('task', 'desc')
    op.add_column('config', sa.Column('remark', mysql.VARCHAR(length=200), nullable=True, comment='测试组的描述'))
    op.drop_column('config', 'desc')
    # ### end Alembic commands ###
