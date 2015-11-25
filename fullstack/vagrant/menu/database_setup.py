# puppies database project for the Udacity course "Full Stack Foundations"
# https://www.udacity.com/course/viewer#!/c-ud088/l-4325204629/m-4294324434

import sqlalchemy

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker, validates
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    #  address = Column(String)
    #  city = Column(String)
    #  state = Column(String(20))
    #  zipCode = Column(String(10))
    #  website = Column(String)
    #  def __repr__(self):
    #     return "<Restaurant(name='%s', Location='%s, %s, %s %s', site='%s')>" % (
    #                          self.name, self.address, self.city, self.state, self.zipCode, self.website)

class MenuItem(Base):
    __tablename__ = 'menuitems'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(10))
    course = Column(Enum('Appetizer','Entree','Dessert','Beverage'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship("Restaurant", backref=backref('menuitems', order_by=name))
    # note: some prices are given with leading "$"
    # use a custom validator to remove those
    # http://docs.sqlalchemy.org/en/rel_1_0/orm/mapped_attributes.html#simple-validators
    @validates('price')
    def validate_price(self, key, value):
        if value[0]=='$':
            return value[1:]
        else:
            return value

DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.create_all(engine)
session.commit()
