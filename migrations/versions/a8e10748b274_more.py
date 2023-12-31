"""more

Revision ID: a8e10748b274
Revises: 1b97dcfc9040
Create Date: 2023-06-25 09:48:03.003505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8e10748b274'
down_revision = '1b97dcfc9040'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_projects_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_projects_timestamp'))
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###
