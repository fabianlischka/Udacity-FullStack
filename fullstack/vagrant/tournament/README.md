# Tournament

A project for the Udacity course [Intro to Relational Databases](https://www.udacity.com/course/viewer#!/c-ud197)

Implement a database to store players and match results for a tournament,
and implement the Swiss system to determine the pairings for the next round.

# Usage overview
1. `vagrant up`  # if necessary to start the VM
1. `vagrant ssh`  # if necessary to ssh into the VM
1. `cd \vagrant\tournament`  # if necessary to change to the project directory
1. `psql -f tournament.sql`  # to create the db
1. `python tournament_test.py`  # to run the tests on the db

# File overview

* `tournament.sql` contains what's necessary to set up the database and views.
* `tournament.py` implements the API to create, delete players, record matches, and
  suggest next pairings
* `tournament_test.py` runs some tests to check the functionality.

# Notes on PostgreSQL

[Here's](http://www.postgresql.org/docs/9.3/interactive/index.html) documentation.

* `createdb <dbname>` in the shell to create a database
* `dropdb <dbname>` in the shell to drop a database
* `psql <dbname>` to connect to and get an interactive SQL session
