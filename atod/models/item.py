from sqlalchemy import Table, Column, Integer

from atod.setup_db import Base
from atod import settings


items = (Column(name, type_) for name, type_ in
                        settings.items_scheme.items() if name != 'ID')


class ItemModel(Base):

    __table__ = Table('items_' + settings.CURRENT_VERSION, Base.metadata,
                      Column('ID', Integer, primary_key=True),
                      *(col for col in items)
                      )

    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)