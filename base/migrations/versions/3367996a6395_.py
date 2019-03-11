"""empty message

Revision ID: 3367996a6395
Revises: 
Create Date: 2019-03-10 13:01:54.751078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3367996a6395'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_email'), 'admin', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admin_email'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
