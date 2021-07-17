Project Overview

This project is a flask app that allows for a user to securely login and sign up to my mock website TrevorMcGlaflin.com.
The user can register for an account by clicking the signup button in the upper left. If they enter an invalid username
or password, they will be reprompted. An invalid username means that there already exists a user with that username. An
invalid password means that it does not fulfill the password requirements: 1 upper and lower case letter, 1 number, one
special character and between 8-25 characters. The user has unlimited attempts to signup but if they are stuggling to
create a valid password they can use the password generator. The password generator is located in the lower left corner
of the page and will autofill the password box with the generated password. It will also display the password on the screen
for the user to copy or write dowm. Once the user has signed up, they will be redirected back to the login page to login
with their new credentials. An existing user can login and if they enter invalid credentials, they will be informed properly.
For instance, if they enter a username that doesn't exist in the database, they will be told that the user name does
not exist. If they enter an existing username but the password is not a match, they will be told so. Once they successully
log in, they will be greeted by a welcoming gif and reward.

Password Protection

To protect the passwords, I started by randomly generating 40 characters of salt and prepending it onto the plaintext.
Then I hashed the salt + the plaintext. Then, I prepended the salt onto the generated hash which is what was stored in
the database. A user is authenticated by first stripping first 40 characters off of the stored hash. Then, prepend that to
the plaintext resulting in a hash that should match the second half of the stored hash.

Running Instructions

1. make sure you have all of the source files including the static and templates directories
2. make sure you have all libraries installed in your virtual environment including:
    - hashlib
    - os
    - base64
    - random
    - sqllite3

3. Setup the database by executing "python3 setup.py". You will notice that a file called user_info.db has been generated
4. Run the flask app by executing "flask run"
5. Navigate to the link that it tells you to go to
