"""fix

Revision ID: 22997731c0df
Revises: 12b80eaf575f
Create Date: 2019-12-17 23:08:59.082950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22997731c0df'
down_revision = '12b80eaf575f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    op.add_column('roles', sa.Column('password_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('roles', 'password_hash')
    op.create_table('books',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('published', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='books_pkey')
    )
    # ### end Alembic commands ###
