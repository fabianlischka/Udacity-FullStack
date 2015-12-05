from contextlib import contextmanager
from database_setup import Restaurant, Base, MenuItem
from flask import Flask, redirect, render_template, request, url_for
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

app = Flask(__name__)

@contextmanager
def db_getSession():
    """Return a DB session connected to the restaurant DB, to use via sqlalchemy."""

    try:
        ## Database connection
        engine = create_engine('sqlite:///restaurantmenu.db')
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        yield session
    except:
        session.rollback() # ???
        raise
    finally:
        # Make the changes to the database persistent
        session.commit()
        # Close communication with the database
        session.close()

# # Database access/interface functions
# def db_getSession():
#     """Return a DB session connected to the restaurant DB, to use via sqlalchemy."""
#     engine = create_engine('sqlite:///restaurantmenu.db')
#     # Bind the engine to the metadata of the Base class so that the
#     # declaratives can be accessed through a DBSession instance
#     Base.metadata.bind = engine
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     return session

# NOTE: the version with trailing _s requires a session as a first param,
# the equivalent version without trailing _s is a convenience method that
# automatically creates the session

def db_listRestaurants():
    """Return a list of restaurant names and ids"""
    with db_getSession() as session:
        return db_listRestaurants_s(session)

def db_listRestaurants_s(session):
    res = [(restaurant.name, restaurant.id) for restaurant in
                            session.query(Restaurant).order_by("name").all()]
    return res


def db_restaurantForId(rid):
    with db_getSession() as session:
        return db_restaurantForId_s(session, rid)

def db_restaurantForId_s(session, rid):
    return session.query(Restaurant).filter_by(id=rid).one()

def db_menuItemForId(mid):
    with db_getSession() as session:
        return db_menuItemForId_s(session, mid)

def db_menuItemForId_s(session, mid):
    return session.query(MenuItem).filter_by(id=mid).one()

def db_newMenuItem(name, restaurant_id, price, description = "Tasty!"):
    with db_getSession() as session:
        newItem = MenuItem( name = name,
                            restaurant_id = restaurant_id,
                            price = price,
                            description = description)
        session.add(newItem)

def db_updateMenuItem(menu_id, name, price, description):
    with db_getSession() as session:
        db_updateMenuItem_s(session, menu_id, name, price, description)

def db_updateMenuItem_s(session, menu_id, name, price, description):
    item = db_menuItemForId_s(session, menu_id)
    print("Need to do something?")
    if (item.name == name and item.price == price
                          and item.description == description):
        print("Nothing to do")
        pass # no change
    else:
        print("Updating")
        item.name = name
        item.price = price
        item.description = description

def db_deleteMenuItem( menu_id ):
    with db_getSession() as session:
        db_deleteMenuItem_s( session, menu_id )

def db_deleteMenuItem_s( session, menu_id ):
    item = db_menuItemForId_s(session, menu_id)
    session.delete(item)


# def listMenuItems():
#     """Return a list of menu items, prices, description"""
#     session = db_getSession()
#     res = [(item.name, item.price, item.description) for item in
#                             session.query(MenuItem).order_by("name").all()]
#     session.close()
#     return res

# def listMenuItemsForId(rid):
#     """Return a list of menu items, prices, description"""
#     session = db_getSession()
#     res = [(item.name, item.price, item.description) for item in
#                             session.query(MenuItem).filter_by(restaurant_id=rid).order_by("name").all()]
#     session.close()
#     return res

# def finddb_restaurantForId(session, rid):
#     """Find restaurant with given id. Returns (Restaurant, errorMsg)"""
#     try:
#         existingRestaurant =  session.query(Restaurant).filter_by(id=rid).one()
#     except NoResultFound:
#         return (None, "Could not find restaurant with id %s." % rid)
#     except MultipleResultsFound:
#         return (None, "Error - multiple restaurants with id %s." % rid)
#     return (existingRestaurant, "")



##### Flask
## rt_ = "route"

@app.route('/')
@app.route('/hello')
def rt_hello():
    output = "<h2>Hello</h2>"
    return output

@app.route('/restaurants/')
def rt_restaurants():
    output = "<h1>Restaurants</h1>"
    output += "<ul>"
    for rname, rid in db_listRestaurants():
        rurl = url_for('rt_restaurants_id', restaurant_id = rid)
        output += "<li><a href='%s'>%s</a></li>" % (rurl, rname)
    output += "</ul>"
    return output

@app.route('/restaurants/<int:restaurant_id>/')
def rt_restaurants_id(restaurant_id):
    with db_getSession() as session:
        restaurant = db_restaurantForId_s(session, restaurant_id)
        items = restaurant.menuitems
        for item in items:
            if not item.price:
                item.price = 999.99
        output = render_template('menu.html', restaurant=restaurant, items=items)
    return output

# Task 1: Create route for rt_newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def rt_newMenuItem(restaurant_id):
    if request.method == 'POST':
        db_newMenuItem( name = request.form['name'],
                        restaurant_id = restaurant_id,
                        price = request.form['price'])
        return redirect(url_for('rt_restaurants_id', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def rt_editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        db_updateMenuItem(  menu_id = menu_id,
                            name = request.form['name'],
                            price = request.form['price'],
                            description = request.form['description'])
        return redirect(url_for('rt_restaurants_id', restaurant_id=restaurant_id))
    else:
        with db_getSession() as session:
            item = db_menuItemForId_s(session, menu_id)
            output = render_template('editMenuItem.html', item=item)
            return output

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def rt_deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        db_deleteMenuItem( menu_id = menu_id )
        return redirect(url_for('rt_restaurants_id', restaurant_id=restaurant_id))
    else:
        with db_getSession() as session:
            item = db_menuItemForId_s(session, menu_id)
            output = render_template('deleteMenuItem.html', item=item)
            return output

if __name__ == '__main__':
    app.debug = True  # NEVER ON PRODUCTION SERVERS
    app.run(host='0.0.0.0', port=5000)
