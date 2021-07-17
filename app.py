"""
Trevor McGlaflin
July 2, 2021
CS 166
Final Project

This is a flask app that allows for a user to securely login to TrevorMcGlaflin.com.
New users have the option to create an account and generate a strong pw if need be.
New users will
"""
import time
from datetime import date
from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
import string
import random
import hashlib
import base64
import os

app = Flask(__name__)

# set secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Set maximum number of attempts to login
MAX_ATTEMPTS = 3
# Special characters to test password strength
SPECIAL_CHAR = "!@#$%^&*"
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 50


# route for home page
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("user_login.html")


# route for when a user attempts to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get('username').strip()
        password = request.form.get('password').strip()

        stored_hash = receive_stored(user_name)
        user_id = get_user_id(user_name)
        if stored_hash is not None:
            if authenticate(stored_hash, password):
                return redirect(url_for('login_success',
                                        id_=user_id))
            flash("Invalid password!", 'alert-danger')
        else:
            flash("Username does not exist!", 'alert-danger')

    return render_template('user_login.html')


# route for when the user succesfully logs in
@app.route("/login_success/<int:id_>", methods=['GET', ])
def login_success(id_):
    flash("Welcome in!!", 'alert-success')
    return render_template('general_home.html')


# route for signup form
@app.route("/signup_form", methods=["GET", "POST"])
def signup_form():
    return render_template("signup.html")


# runs when user submits signup form
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # collect password and username from user input
        user_name = request.values["username"]
        password = request.values["password"]

        # check if the password is strong enough and if the user name is unique
        if password_strength(password) and unique_user_name(user_name):
            add_user(user_name, password, 1)
            flash("Successfully registered... please login with your credentials.", 'alert-success')
            return render_template("user_login.html")

        # display proper message if user entered invalid username or password
        if not unique_user_name(user_name):
            flash("Oh no... Username already exists! Please use a different user name.", 'alert-danger')
        flash("Password is not strong enough... look at rules above and try again.", 'alert-danger')
    return render_template("signup.html")


# generates a strong password for the user from the proper character set
@app.route("/generate_pw", methods=["GET", "POST"])
def generate_pw():
    if request.method == "POST":
        password_length = int((PASSWORD_MAX_LENGTH + PASSWORD_MIN_LENGTH) / 2)
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(15))
        return render_template("signup.html", generated_pw=password)


# checks if user name is unique (returns false if it already exists)
def unique_user_name(user_name):
    data = query_db()
    for dati in data:
        if dati[0] == user_name:
            return False
    return True


# tests password strength (returns bool)
def password_strength(test_password) -> bool:
    if test_password.isalnum() or test_password.isalpha():
        return False
    if len(test_password) < PASSWORD_MIN_LENGTH:
        return False
    if len(test_password) > PASSWORD_MAX_LENGTH:
        return False
    special_char_check = False
    has_upper = False
    has_lower = False
    has_digit = False
    for ch in test_password:
        if ch in SPECIAL_CHAR:
            special_char_check = True
        if ch.isupper():
            has_upper = True
        if ch.islower():
            has_lower = True
        if ch.isdigit():
            has_digit = True
    if not special_char_check or \
            not has_upper or \
            not has_lower or \
            not has_digit:
        return False
    else:
        return True


# adds user to database
def add_user(user_name, password, access_level):
    # encode and hash password
    salt = str(base64.b64encode(os.urandom(40)))
    hashable = salt + password
    hashable = hashable.encode('utf-8')
    this_hash = hashlib.sha1(hashable).hexdigest()
    salt_prepended_hash = salt + this_hash
    data_to_insert = [(user_name, salt_prepended_hash, access_level)]
    try:
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        c.executemany("INSERT INTO user_info (user_name, password, access_level) VALUES (?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


# check for login attempts on same day
def check_logins(user_name):
    try:
        data_rows = []
        conn = sqlite3.connect('login_attempt.db')
        c = conn.cursor()
        return c.execute("SELECT COUNT(*) FROM login_attempts WHERE ").fetchall()
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

# returns a list of the data in the query
def query_db():
    try:
        data_rows = []
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        return c.execute("SELECT * FROM user_info").fetchall()
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


# retrieves a stored password salt + hash from database, given a username
def receive_stored(user_name):
    data = query_db()
    for dati in data:
        if dati[0] == user_name:
            return dati[1]
    return None


# retreives the user id pk from database given a username
def get_user_id(user_name):
    data = query_db()
    for dati in data:
        if dati[0] == user_name:
            return dati[3]
    return None


# authenticates password
def authenticate(stored, plain_text, salt_length=59) -> bool:
    salt_length = salt_length
    salt = stored[:salt_length]
    stored_hash = stored[salt_length:]
    hashable = salt + plain_text
    hashable = hashable.encode('utf-8')
    this_hash = hashlib.sha1(hashable).hexdigest()
    return this_hash == stored_hash










