from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Restaurant, Base, MenuItem
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# AGENDA:
# need to close sessions?

def getSession():
    """Return a DB session connected to the restaurant DB, to use via sqlalchemy."""
    engine = create_engine('sqlite:///restaurantmenu.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()
    return session

# handler: what to do based on requests received
class FabsFirstHandler(BaseHTTPRequestHandler):
    pattern_edit = re.compile("/restaurants/([0-9]+)/edit")
    pattern_delete = re.compile("/restaurants/([0-9]+)/delete")

    def do_GET(self):
        """Handle GET requests."""
        try:
            # match and determine the appropriate output
            if self.path.endswith("/restaurants"):
                output = restaurantOutput()
            elif self.path.endswith("/restaurants/new"):
                output = restaurantNewOutput()
            elif self.pattern_edit.match(self.path):
                id = self.pattern_edit.match(self.path).group(1)
                output = restaurantEditOutput(id)
            elif self.pattern_delete.match(self.path):
                id = self.pattern_delete.match(self.path).group(1)
                output = restaurantDeleteOutput(id)
            elif self.path.endswith("/hello"):
                output = helloOutput()
            elif self.path.endswith("/hola"):
                output = holaOutput()
            else:  # or raise IOError if nothing matched
                raise IOError
            # then write that output to the client
            self.write_text_output(output)

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def write_text_output(self, output, response_code = 200, debug = True):
        """Return standard HTML text output."""
        self.send_response(response_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(output)
        if debug:
            print output
        return

    def do_POST(self):
        """Handle POST requests."""
        # NOTE: Have disabled the try..except block for now,
        # for debugging purposes, to see exceptions thrown further down
        # try:
        if self.path.endswith("/hello"):
            messagecontent = self.getField('mmmessage')
            output = postHelloOutput(messagecontent)
            self.write_text_output(output, response_code=301)
        elif self.path.endswith("/restaurants/new"):
            messagecontent = self.getField('rname')
            status = addNewRestaurant(messagecontent)
            output = postRestaurantNewOutput(messagecontent, status)
            # the output above leaves us on this page, with a confirmation that
            # the restaurant had been added.
            # alternatively, uncomment the line below, to
            # be sent back to /restaurants instead
#            self.send_header('Location', '/restaurants')
            self.write_text_output(output, response_code=301)
        elif self.pattern_edit.match(self.path):
            rid = self.pattern_edit.match(self.path).group(1)
            rName = self.getField('rname')
            status = changeRestaurantName(rid, rName)
            output = postRestaurantEditOutput(rid, status)
            self.write_text_output(output, response_code=301)
        elif self.pattern_delete.match(self.path):
            rid = self.pattern_delete.match(self.path).group(1)
            status = deleteRestaurantWithId(rid)
            output = postRestaurantDeleteOutput(rid, status)
            self.write_text_output(output, response_code=301)


        # except:
        #     pass

    def getField(self, fieldname):
        messagecontent=''  # sentinel for unknown
        ctype, pdict = cgi.parse_header(
            self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get(fieldname)
        return messagecontent[0]

# DB interface functions
def listRestaurants():
    """Return a list of restaurant names and ids"""
    session = getSession()
    res = [(restaurant.name, restaurant.id) for restaurant in
                            session.query(Restaurant).order_by("name").all()]
    session.close()
    return res

def findRestaurantForId(session, rid):
    """Find restaurant with given id. Returns (Restaurant, errorMsg)"""
    try:
        existingRestaurant =  session.query(Restaurant).filter_by(id=rid).one()
    except NoResultFound:
        return (None, "Could not find restaurant with id %s." % rid)
    except MultipleResultsFound:
        return (None, "Error - multiple restaurants with id %s." % rid)
    return (existingRestaurant, "")

def addNewRestaurant(restaurantName):
    """Add a new restaurant to the DB, unless name exists already, then do nothing"""
    session = getSession()
    existingRestaurants = [restaurant.name for restaurant in
                            session.query(Restaurant).find_by(name=restaurantName).all()]
    if restaurantName in existingRestaurants:
        return  "Restaurant with name %s exists already." % restaurantName
    myNewRestaurant = Restaurant(name = restaurantName)
    session.add(myNewRestaurant)
    session.commit()
    session.close()
    return "OK - Restaurant with name %s added successfully." % restaurantName

def changeRestaurantName(rid, rName):
    """Change name of restaurant with id 'rid' to 'rName'."""
    session = getSession()
    existingRestaurant, errorMsg = findRestaurantForId(session, rid)
    if existingRestaurant:
        existingRestaurant.name = rName
        session.add(existingRestaurant)
        session.commit()
        session.close()
        return "OK - Changed restaurant name to %s." % rName
    else:
        session.close()
        return errorMsg

def deleteRestaurantWithId(rid):
    session = getSession()
    existingRestaurant, errorMsg = findRestaurantForId(session, rid)
    if existingRestaurant:
        session.delete(existingRestaurant)
        session.commit()
        session.close()
        return "OK - Deleted restaurant with id %s." % rid
    else:
        session.close()
        return errorMsg

# output GET functions
def helloOutput():
    output = ""
    output += "<html><body>"
    output += "<h1>Hello! <a href='/restaurants'>Let's go to the restaurants...</a></h1>"
    output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="mmmessage" type="text" ><input type="submit" value="Submit"> </form>'''
    output += "</body></html>"
    return output

def holaOutput():
    output = ""
    output += "<html><body>"
    output += "<h1>&#161 Hola !</h1>"
    output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="mmmessage" type="text" ><input type="submit" value="Submit"> </form>'''
    output += "</body></html>"
    return output

def restaurantOutput():
    output = ""
    output += "<html><body>"
    output += " <h1> List of Restaurants</h1>"
    output += " <ul>"
    for restaurant_name, restaurant_id in listRestaurants():
        output += " <li> %s </li>" % restaurant_name
        output += " <a href='/restaurants/%s/edit'>Edit</a>" % restaurant_id
        output += " <a href='/restaurants/%s/delete'>Delete</a>" % restaurant_id
    output += " </ul>"
    output += "<h3>Want to add a new restaurant?</h3>"
    output += "<p>You can <a href='/restaurants/new'>add a new restaurant here.</a></p>"
#        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="mmmessage" type="text" ><input type="submit" value="Submit"> </form>'''  # noqa
    output += "</body></html>"
    return output

def restaurantNewOutput():
    output = ""
    output += "<html><body>"
    output += " <h1> Add a New Restaurant</h1>"
    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>What is the name of the new restaurant?</h2><input name="rname" type="text" ><input type="submit" value="Submit"> </form>'''
    output += "<p>No thanks, <a href='/restaurants'>take me back to the list of restaurants</a>.</p>"
    output += "<h3>Below the list of restaurants we know already! :-)</h3>"
    output += " <ul>"
    for restaurant_name, restaurant_id in listRestaurants():
        output += " <li> %s </li>" % restaurant_name
    output += " </ul>"
    output += "</body></html>"
    return output

def restaurantEditOutput(rid):
    session = getSession()
    (restaurant, errorMsg) = findRestaurantForId(session, rid)
    output = ""
    output += "<html><body>"
    output += " <h1>Change Restaurant Name</h1>"
    if restaurant:
        rName = restaurant.name
        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % rid
        output += "<h2>What is the new name of the restaurant previously known as %s?</h2>" % rName
        output += "<input name='rname' type='text'>"
        output += "<input type='submit' value='Submit'> </form>"
        output += "<p>No thanks, <a href='/restaurants'>take me back to the list of restaurants</a>.</p>"
    else:
        output += "<p>Sorry, there was a problem: %s </p>" % errorMsg
        output += "<p>Oops, <a href='/restaurants'>take me back to the list of restaurants</a>.</p>"
    output += "</body></html>"
    session.close()
    return output

def restaurantDeleteOutput(rid):
    session = getSession()
    (restaurant, errorMsg) = findRestaurantForId(session, rid)
    output = ""
    output += "<html><body>"
    output += " <h1>Delete Restaurant</h1>"
    if restaurant:
        rName = restaurant.name
        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" %rid
        output += "<h2>Are you sure you want to delete restaurant %s?</h2>" % rName
        output += "<button type='submit' value='Delete'>DELETE</button> </form>"
        output += "<p>No thanks, <a href='/restaurants'>take me back to the list of restaurants</a>.</p>"
    else:
        output += "<p>Sorry, there was a problem: %s </p>" % errorMsg
        output += "<p>Oops, <a href='/restaurants'>take me back to the list of restaurants</a>.</p>"
    output += "</body></html>"
    return output

# output POST functions

def postHelloOutput(messagecontent):
    output = ""
    output += "<html><body>"
    output += " <h2> Okay, how about this: </h2>"
    output += "<h1> %s </h1>" % messagecontent
    output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="mmmessage" type="text" ><input type="submit" value="Submit"> </form>'''  # noqa
    output += "</body></html>"
    return output

def postRestaurantNewOutput(messagecontent, rstatus):
    output = ""
    output += "<html><body>"
    output += " <h1> %s </h1>" % rstatus
    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Want to add another restaurant?</h2><input name="rname" type="text" ><input type="submit" value="Submit"> </form>'''
    output += "<p>No thanks, <a href='/restaurants'>take me back to the list of restaurants</a>.</p>"
    output += "<h3>Below the list of restaurants we know already! :-)</h3>"
    output += " <ul>"
    for restaurant_name, restaurant_id in listRestaurants():
        output += " <li> %s </li>" % restaurant_name
    output += " </ul>"
    output += "</body></html>"
    return output

def postRestaurantEditOutput(messagecontent, rstatus):
    output = ""
    output += "<html><body>"
    output += " <h1> %s </h1>" % rstatus
    output += "<p>Thanks, <a href='/restaurants'>take me back to the list of restaurants</a>.</p>"
    output += "<h3>Below the list of restaurants we know now! :-)</h3>"
    output += " <ul>"
    for restaurant_name, restaurant_id in listRestaurants():
        output += " <li> %s </li>" % restaurant_name
    output += " </ul>"
    output += "</body></html>"
    return output

def postRestaurantDeleteOutput(messagecontent, rstatus):
    output = ""
    output += "<html><body>"
    output += " <h1> %s </h1>" % rstatus
    output += "<p>Thanks, <a href='/restaurants'>take me back to the list of restaurants</a>.</p>"
    output += "<h3>Below the list of restaurants we know now! :-)</h3>"
    output += " <ul>"
    for restaurant_name, restaurant_id in listRestaurants():
        output += " <li> %s </li>" % restaurant_name
    output += " </ul>"
    output += "</body></html>"
    return output

# main: instantiates, and determines on what port to listen
def main():
    try:
        port = 8080
        server = HTTPServer(('',port), FabsFirstHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt():
        print "Interrupt received, closing server..."
        server.socket.close()

if __name__ == '__main__':
    main()
