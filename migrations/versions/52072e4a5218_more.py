"""more

Revision ID: 52072e4a5218
Revises: a6d5bfb7bda1
Create Date: 2023-06-28 08:21:25.637904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52072e4a5218'
down_revision = 'a6d5bfb7bda1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
