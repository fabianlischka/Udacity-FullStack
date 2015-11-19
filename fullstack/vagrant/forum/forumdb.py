# baby project for the Udacity course "Intro to Relational Databases"
# https://www.udacity.com/course/viewer#!/c-ud197
#
# Database access functions for the web forum.
#

import bleach
from contextlib import contextmanager
import psycopg2
import time


@contextmanager
def DBCur():
    ## Database connection
    conn = psycopg2.connect("dbname=forum")
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


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    # select content, time from forum order by time desc
    with DBCur() as cur:
        # Query the database and obtain data as Python objects
        cur.execute("SELECT content, time FROM posts ORDER BY time DESC;")
        DB = cur.fetchall()

    posts = [{'content': str(row[0]), 'time': str(row[1])} for row in DB]
#    posts.sort(key=lambda row: row['time'], reverse=True)
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    # t = time.strftime('%c', time.localtime())
    # DB.append((t, content+" Arrrr!"))
    content = bleach.clean(content)
    with DBCur() as cur:
        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no more SQL injections!)
        cur.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
