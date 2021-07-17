"""
Trevor McGlaflin
July 7, 2021
CS 166
Final Project

This file will set up the database for the flask app.
"""
import sqlite3


def create_db():
    try:
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE user_info
                    (
                    user_name text NOT NULL,
                    password text NOT NULL,
                    access_level integer NOT NULL,
                    ID INTEGER PRIMARY KEY AUTOINCREMENT
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


# call the function
create_db()












