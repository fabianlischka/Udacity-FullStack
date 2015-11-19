# puppies database project for the Udacity course "Full Stack Foundations"
# https://www.udacity.com/course/viewer#!/c-ud088/l-4325204629/m-4294324434

import sqlalchemy

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# engine = create_engine('sqlite:///puppies.db')
# # Bind the engine to the metadata of the Base class so that the
# # declaratives can be accessed through a DBSession instance
# Base.metadata.bind = engine
#
# DBSession = sessionmaker(bind=engine)
# # A DBSession() instance establishes all conversations with the database
# # and represents a "staging zone" for all the objects loaded into the
# # database session object. Any change made against the objects in the
# # session won't be persisted into the database until you call
# # session.commit(). If you're not happy about the changes, you can
# # revert all of them back to the last commit by calling
# # session.rollback()
#
# session = DBSession()


class Shelter(Base):
     __tablename__ = 'shelters'
     id = Column(Integer, primary_key=True)
     name = Column(String, nullable=False)
     address = Column(String)
     city = Column(String)
     state = Column(String(20))
     zipCode = Column(String(10))
     website = Column(String)
     def __repr__(self):
        return "<Shelter(name='%s', Location='%s, %s, %s %s', site='%s')>" % (
                             self.name, self.address, self.city, self.stat, self.zipCode, self.website)

class Puppy(Base):
     __tablename__ = 'puppies'
     id = Column(Integer, primary_key=True)
     name = Column(String, nullable=False)
     dateOfBirth = Column(Date)
     gender = Column(Enum('male','female'))
     weight = Column(Numeric(10))
     picture = Column(String)
     shelter_id = Column(Integer, ForeignKey('shelters.id'))
     shelter = relationship("Shelter", backref=backref('puppies', order_by=name))




# ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
# session.add(ed_user)
# session.add_all([
#      User(name='wendy', fullname='Wendy Williams', password='foobar'),
#      User(name='mary', fullname='Mary Contrary', password='xxg527'),
#      User(name='fred', fullname='Fred Flinstone', password='blah')])
# session.commit()
#
