"""create posts table

Revision ID: fea3c2734352
Revises: 
Create Date: 2023-07-29 13:35:09.209406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fea3c2734352'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('title', sa.String, nullable=False),
                    sa.Column('content', sa.String, nullable=False),
                    sa.Column('published', sa.Boolean, server_default="True", nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP, onupdate=sa.text('now()'), nullable=True),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('posts')
