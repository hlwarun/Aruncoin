from flask import Flask, redirect, request, session, url_for, logging, render_template, flash
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import config
import forms

app = Flask(__name__)

# Configuring settings for MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = config._mysql_user
app.config['MYSQL_PASSWORD'] = config._mysql_password
app.config['MYSQL_DB'] = config._mysql_db
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # This means we are accessing informations by dictionaries

db = MySQL(app)

# This databse.py should be imported below db = MySQL(app)
# If imported above db cannot be imported back to database.py
import database


# Creating a route for the home page
@app.route('/')
def home():
    # database.delete_table_items()
    return render_template('index.html')

# Creating a route for the about page
@app.route('/about/')
def about():
    return render_template('about.html', title="About")

# Creating a route for the contact page
@app.route('/contact/')
def contact():
    return render_template('contact.html', title="Contact Us")

# Creating a route for the about page
def login_get(username):
    users = database.Table("users", "first_name", "last_name", "username", "email", "password")
    user = users.getone('username', username)

    session['logged_in'] = True
    session['username'] = username
    session['first_name'] = user.get('first_name')
    session['last_name'] = user.get('last_name')
    session['email'] = user.get('email')

    # return render_template('login.html')

# Creating a route for the register page
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm(request.form)
    users = database.Table("users", "first_name", "last_name", "username", "email", "password")

    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data

        if database.isnewuser(username):
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(first_name, last_name, username, email, password)
            login_get(username)
            return redirect(url_for('dashboard'))
        else:
            flash('User with this username already exists. Please try again with different username!', 'danger')
            return redirect(url_for('register'))

    return render_template('signup.html', title="Sign Up", form=form)

# Creating a route for the dashboard page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user_password = request.form['password']

        users = database.Table("users", "first_name", "last_name", "username", "email", "password")
        user = users.getone('username', username)
        db_password = user.get('password')

        if db_password is None:
            flash('User with this username does not exists!', 'danger')
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(user_password, db_password):
                login_get(username)
                flash('Congratulations! You have been logged in to your account.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect Password!', 'danger')
                return redirect(url_for('login'))

    return render_template('login.html', title="Login")


# Creating a route for the dashboard page
@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html', title="Dashboard", session=session)

# If we run the FLASK APP as main run the app
if __name__ == '__main__':
    app.secret_key = config._app_key
    app.run(debug=True, port=8000)
