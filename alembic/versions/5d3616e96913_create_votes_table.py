"""create votes table

Revision ID: 5d3616e96913
Revises: 
Create Date: 2023-07-29 14:41:23.080429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d3616e96913'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('post_id', sa.Integer, nullable=False),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('post_id', 'user_id'))


def downgrade() -> None:
    op.drop_table(table_name='votes')
