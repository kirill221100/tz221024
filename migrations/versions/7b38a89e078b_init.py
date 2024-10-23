"""init

Revision ID: 7b38a89e078b
Revises: 
Create Date: 2024-10-23 15:41:34.312580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b38a89e078b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('register_ref_code_id', sa.Integer(), nullable=True),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    #sa.ForeignKeyConstraint(['register_ref_code_id'], ['referral_codes.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('referral_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('referrer_id', sa.Integer(), nullable=False),
    sa.Column('exp_date', sa.DateTime(), nullable=False),
    #sa.ForeignKeyConstraint(['referrer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_foreign_key('fk_user_referral_codes', 'users', 'referral_codes',
                          ['register_ref_code_id'], ['id'])
    op.create_foreign_key('fk_referral_code_users', 'referral_codes', 'users',
                          ['referrer_id'], ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('referral_codes')
    # ### end Alembic commands ###