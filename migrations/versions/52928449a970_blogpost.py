"""blogpost

Revision ID: 52928449a970
Revises: d13b279593ec
Create Date: 2023-06-23 11:07:43.587355

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '52928449a970'
down_revision = 'd13b279593ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_blog_posts_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index('ix_posts_timestamp')

    op.drop_table('posts')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('body', mysql.TEXT(), nullable=True),
    sa.Column('timestamp', mysql.DATETIME(), nullable=True),
    sa.Column('author_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name='posts_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_index('ix_posts_timestamp', ['timestamp'], unique=False)

    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_blog_posts_timestamp'))

    op.drop_table('blog_posts')
    # ### end Alembic commands ###
