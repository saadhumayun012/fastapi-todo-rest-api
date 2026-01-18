"""Add phone number column to user model

Revision ID: 82cc231b0bc0
Revises: 
Create Date: 2026-01-18 20:01:00.673340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82cc231b0bc0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # adding a phone number column to the users model
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True)) 


def downgrade() -> None:
    """Downgrade schema."""
    # op.alter_column('users', 'phone_number')
