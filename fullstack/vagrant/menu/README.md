# Restaurant Menu - Data Driven Webserver

This is a small database and web server project for
the [Udacity course "Full Stack Foundations".]
(https://www.udacity.com/course/viewer#!/c-ud088/l-4325204629/m-4294324434)

# Usage overview
1. `vagrant up`  # if necessary to start the VM
1. `vagrant ssh`  # if necessary to ssh into the VM
1. `cd \vagrant\menu`  # if necessary to change to the project directory
1. `python lotsofmenus.py`  # if necessary to create the db and populate it
1. `python webserver.py`  # to run the webserver
1. Go to http://localhost:8080/hello in your browser

# File overview
* `CRUD-overview.md` - just a few basics on performing CRUD with sqlalchemy
* `database_setup.py` - definitions of the objects used in sqlalchemy ORM,
  and setup of the database
* `lotsofmenus.py` - used to pupulate the database of restaurants and menu items
* `restaurantmenu.db` - the SQLite database (might not be in the repository,
  but created and populated by the above)
* `webserver.py` - very simple webserver, using only Python's basic
  BaseHTTPRequestHandler, HTTPServer
