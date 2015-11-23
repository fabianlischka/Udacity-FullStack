from sqlalchemy import *
from migrate import *

from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

profile = Table(
    'account', meta,
    Column('id', Integer, primary_key=True),
    Column('login', String(40)),
    Column('passwd', String(40)),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    account.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    account.drop()

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
