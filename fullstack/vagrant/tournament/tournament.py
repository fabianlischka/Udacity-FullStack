#!/usr/bin/env python
#
# tournament project for the Udacity course "Intro to Relational Databases"
# https://www.udacity.com/course/viewer#!/c-ud197
#
# tournament.py -- implementation of a Swiss-system tournament
#

from contextlib import contextmanager
from itertools import izip
import psycopg2

def ipairs(seq):
    it = iter(seq)
    return izip(it, it)

@contextmanager
def DBCur(dbname):
    ## Database connection
    conn = psycopg2.connect("dbname=%s" % dbname)
    try:
        # Open a cursor to perform database operations
        cur = conn.cursor()
        yield cur
    except:
        conn.rollback()
        raise
    finally:
        # Make the changes to the database persistent
        conn.commit()
        # Close communication with the database
        cur.close()
        conn.close()



# def connect():
#     """Connect to the PostgreSQL database.  Returns a database connection."""
#     return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    with DBCur("tournament") as cur:
        cur.execute("DELETE FROM games;")

def deletePlayers():
    """Remove all the player records from the database."""
    with DBCur("tournament") as cur:
        cur.execute("DELETE FROM players;")


def countPlayers():
    """Returns the number of players currently registered."""
    with DBCur("tournament") as cur:
        cur.execute("SELECT count(*) FROM players;")
        DB = cur.fetchone()
    return int(DB[0])

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with DBCur("tournament") as cur:
        cur.execute("INSERT INTO players VALUES (%s);", (name,))

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with DBCur("tournament") as cur:
        cur.execute("SELECT * FROM standing;");
        DB = cur.fetchall()
    return DB

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with DBCur("tournament") as cur:
        cur.execute("INSERT INTO games VALUES (%s, %s, %s);", (1, winner, loser))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    return [(a+b) for a,b in izip(*[iter( [(id,name) for id,name,w,m in playerStandings()] )]*2)]
