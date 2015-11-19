from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy

from datetime import date, timedelta

engine = create_engine('sqlite:///puppies.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

print "1. Query all of the puppies and return the results in ascending alphabetical order"
for puppy in session.query(Puppy).order_by(Puppy.name):
     print puppy.name, puppy.gender, puppy.shelter.name
print "\n\n"

print "2. Query all of the puppies that are less than 6 months old organized by the youngest first"
print "Note: will find puppies not more than 180 days old."
cutoffDate = date.today() - timedelta(days=180)
for puppy in session.query(Puppy).filter(Puppy.dateOfBirth>=cutoffDate).order_by(desc(Puppy.dateOfBirth)):
    print puppy.name, puppy.dateOfBirth
print "\n\n"

print "3. Query all puppies by ascending weight"
for puppy in session.query(Puppy).order_by(Puppy.weight):
    print puppy.name, puppy.weight
print "\n\n"

print "4. Query all puppies grouped by the shelter in which they are staying"
for shelter in session.query(Shelter).all():
    print "\n", shelter.name
    for puppy in shelter.puppies:
        print "\t", puppy.name
print "\n\n"
