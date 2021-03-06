"""post table

Revision ID: c3beefb8fe40
Revises: 55291716bf8c
Create Date: 2020-04-05 04:12:39.975223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3beefb8fe40'
down_revision = '55291716bf8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'content',
               existing_type=sa.VARCHAR(length=140),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'content',
               existing_type=sa.VARCHAR(length=140),
               nullable=True)
    # ### end Alembic commands ###
