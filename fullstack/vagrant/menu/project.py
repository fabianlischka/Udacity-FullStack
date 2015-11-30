from database_setup import Restaurant, Base, MenuItem
from flask import Flask, render_template, url_for
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

app = Flask(__name__)

# Database access/interface functions
def getSession():
    """Return a DB session connected to the restaurant DB, to use via sqlalchemy."""
    engine = create_engine('sqlite:///restaurantmenu.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def listRestaurants():
    """Return a list of restaurant names and ids"""
    session = getSession()
    res = [(restaurant.name, restaurant.id) for restaurant in
                            session.query(Restaurant).order_by("name").all()]
    session.close()
    return res

def restaurantForId(rid):
    session = getSession()
    res = session.query(Restaurant).filter_by(id=rid).one()
    # session.close()
    return res

# def listMenuItems():
#     """Return a list of menu items, prices, description"""
#     session = getSession()
#     res = [(item.name, item.price, item.description) for item in
#                             session.query(MenuItem).order_by("name").all()]
#     session.close()
#     return res

# def listMenuItemsForId(rid):
#     """Return a list of menu items, prices, description"""
#     session = getSession()
#     res = [(item.name, item.price, item.description) for item in
#                             session.query(MenuItem).filter_by(restaurant_id=rid).order_by("name").all()]
#     session.close()
#     return res

# def findRestaurantForId(session, rid):
#     """Find restaurant with given id. Returns (Restaurant, errorMsg)"""
#     try:
#         existingRestaurant =  session.query(Restaurant).filter_by(id=rid).one()
#     except NoResultFound:
#         return (None, "Could not find restaurant with id %s." % rid)
#     except MultipleResultsFound:
#         return (None, "Error - multiple restaurants with id %s." % rid)
#     return (existingRestaurant, "")



##### Flask

@app.route('/')
@app.route('/hello')
def op_hello():
    output = "<h2>Hello</h2>"
    return output

@app.route('/restaurants/')
def op_restaurants():
    output = "<h1>Restaurants</h1>"
    output += "<ul>"
    for rname, rid in listRestaurants():
        rurl = url_for('op_restaurants_id', restaurant_id = rid)
        output += "<li><a href='%s'>%s</a></li>" % (rurl, rname)
    output += "</ul>"
    return output

@app.route('/restaurants/<int:restaurant_id>/')
def op_restaurants_id(restaurant_id):
    restaurant = restaurantForId(restaurant_id)
    items = restaurant.menuitems
    return render_template('menu.html', restaurant=restaurant, items=items)
    # output += "<ul>"
    # for name, price, description in listMenuItemsForId(restaurant_id):
    #     output += "<li>%s - %s<br>%s</li>" % (name, price, description)
    # output += "</ul>"

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True  # NEVER ON PRODUCTION SERVERS
    app.run(host='0.0.0.0', port=5000)
