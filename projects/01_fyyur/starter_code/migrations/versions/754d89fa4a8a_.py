"""empty message

Revision ID: 754d89fa4a8a
Revises: fe7103f30256
Create Date: 2023-02-14 00:52:36.769012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '754d89fa4a8a'
down_revision = 'fe7103f30256'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('seeking_yn', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('seeking_desc', sa.String(length=1000), nullable=True))

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('seeking_yn', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('seeking_desc', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.drop_column('seeking_desc')
        batch_op.drop_column('seeking_yn')
        batch_op.drop_column('website')

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_column('seeking_desc')
        batch_op.drop_column('seeking_yn')
        batch_op.drop_column('website')

    op.drop_table('Show')
    # ### end Alembic commands ###
