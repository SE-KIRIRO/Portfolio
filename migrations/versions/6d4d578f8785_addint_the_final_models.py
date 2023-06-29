"""addint the final models

Revision ID: 6d4d578f8785
Revises: 60284c16f84d
Create Date: 2023-06-28 15:13:00.599877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d4d578f8785'
down_revision = '60284c16f84d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pictures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('picture_file', sa.String(length=128), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('developer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['developer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('thumbnail_file', sa.String(length=64), nullable=False),
    sa.Column('video_link', sa.String(length=128), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('developer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['developer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('videos')
    op.drop_table('pictures')
    # ### end Alembic commands ###
