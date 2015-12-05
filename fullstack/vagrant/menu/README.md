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
1. `python project.py`  # to run the new and improved Flask webserver
1. Go to http://localhost:5000/ in your browser

# File overview
* `CRUD-overview.md` - just a few basics on performing CRUD with sqlalchemy
* `database_setup.py` - definitions of the objects used in sqlalchemy ORM,
  and setup of the database
* `lotsofmenus.py` - used to pupulate the database of restaurants and menu items
* `restaurantmenu.db` - the SQLite database (might not be in the repository,
  but created and populated by the above)
* `webserver.py` - very simple webserver, using only Python's basic
  BaseHTTPRequestHandler, HTTPServer. Basically for study purposes, but obsolete.
* `project.py` - more complete webserver, using Flask.
* `project-template.py` - provided in the instructor notes, used as a template
  to copy some things into `project.py`

# notes on Flask

Documentation for [Flask](http://flask.pocoo.org/docs/) and [Jinja](http://jinja.pocoo.org/docs/).

Useful:
* decorator to route URL requests, including variable substitution:
  * Example:
```
@app.route('/profile/<username>')
    def profile(username):
```
* `url_for` to build URLs
  * example: `url_for('profile', username='John Doe')`̨
* `render_template` to "execute" and render a html template
  * example: `render_template('hello.html', name=name)`
