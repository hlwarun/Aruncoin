from flask import Flask, redirect, request, session, url_for, logging, render_template, flash
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import config

app = Flask(__name__)

# Configuring settings for MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = config._mysql_user
app.config['MYSQL_PASSWORD'] = config._mysql_password
app.config['MYSQL_DB'] = config._mysql_db
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # This means we are accessing informations by dictionaries

db = MySQL(app)

# Creating a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Creating a route for the about page
@app.route('/about/')
def about():
    return render_template('about.html')

# Creating a route for the about page
@app.route('/contact/')
def contact():
    return render_template('contact.html')

# If we run the FLASK APP as main run the app
if __name__ == '__main__':
    app.secret_key = config._app_key
    app.run(debug=True, port=8000)
