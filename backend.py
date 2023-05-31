from flask import Flask, flash, redirect, render_template, url_for, request, session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select, column, Boolean, table, insert, delete
from sqlalchemy.orm import sessionmaker

from flask_migrate import Migrate
import json, hashlib, sys, re, configparser

SESSION_TYPE = 'sqlalchemy'

# TODO ->

# 1
# Change blocklists dashboard behaviour
# Making an actual dashboard

# 2
## Adding Migrations to this project directory
# Also testing that the migrations work

# 3
## Create blocked domains app route and functionality
# It works by this following path: -> Before Update-blocklist writes to a file it also writes to a new database table.
# Then i read that table in the backend.py and display it in the frontend.

# 4
## Create a page as 'block domains' aka block specific websites manually.

# <- TODO

def checkLoggedIn():
   # checks if key exists and if its value is set to true
   if 'logged_in' in session and session['logged_in'] == True:
     return False
   else:
      return redirect(url_for('login'))

def hashing(password):
   return hashlib.sha256(password.encode('utf-8')).hexdigest()

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini') # Reads config file

app.secret_key = config.get('internal', 'secret_key')

# Creating a low level connection to the database to retrieve adlists data
db_params = config['database']
db_uri = f"mysql://{db_params['username']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database_name']}"
engine = create_engine(db_uri)

# Adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# This worked because of 'mysqlclient' package/driver from the pypi repo's
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an SQL-Alchemy instance
db = SQLAlchemy(app)

# Migrate
migrate = Migrate(app, db)

# Inter
mysqlSession = sessionmaker(bind=engine)
mysql_session = mysqlSession()

adlists_table = table("adlists",
        column("id"),
        column("type"),
        column("url"),
)

# Flask route definitions and functions

@app.route('/')
def index():
   return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():

   # Checks if we need to redirect the user to the login page
   # Assigns the return of checkLoggedIn() to a variable and checks if it evaluates to true at the same time
   if url := checkLoggedIn():
      return url

   return render_template('dashboard.html')

@app.route('/blocklists')
def blocklists():
   if url := checkLoggedIn():
      return url

   result = engine.execute('SELECT * FROM adlists')
   rows = result.fetchall()

   return render_template('blocklists.html', data=rows)

@app.route('/blocked-domains')
def blockedDomains():
   if url := checkLoggedIn():
      return url

   return render_template('blocked-domains.html')

@app.route('/login', methods=['get'])
def login():
   return render_template('login.html')

# post route; formular data of the login page gets sent here
@app.route('/login', methods=['post'])
def checkCredentials():
   pepper = config.get('internal', 'pepper')

   users_password_with_salt_and_pepper = request.form['passwd'] + config.get('internal', 'salt') + pepper
   users_password_salted_peppered_and_hashed = hashing(users_password_with_salt_and_pepper)

   if config.get('auth', 'username') == request.form['username'] and config.get('auth', 'password_hashed') == users_password_salted_peppered_and_hashed:
      session['logged_in'] = True
      return redirect(url_for('dashboard'))
   else:
      return render_template('login.html', error="Error, you inputted the wrong username or password. Please try again.")

# post route; formular data to add blocklists goes here
@app.route('/blocklist/add', methods=['post'])
def addBlocklist():
   if url := checkLoggedIn():
      return url

   type = request.form.get('type')
   url = request.form.get('url')

   # validate user input: type
   if type not in ['hosts', 'adblock']:
      return "Invalid Input"

   # validate user input: url; checking if valid url that can be safely inserted into the database
   url_regex = r'^https?://([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z0-9]+(-[a-z0-9]+)*(:\d+)?(/[\w./?%&=-]*)?$'

   matches_url = re.search(url_regex, url)
   if matches_url is None:
      return "Invalid"

   # SQLAlchemy query to add blocklist
   adlists = insert(adlists_table).values(type=type, url=url)
   engine.execute(adlists)

   return redirect(url_for('blocklists'))

# post request; deletes a specific blocklist
@app.route('/blocklist/delete/<int:id>', methods=['post'])
def deleteBlocklist(id):
   if url := checkLoggedIn():
      return url

   adlists = delete(adlists_table).where(adlists_table.c.id == id)
   engine.execute(adlists)

   return redirect(url_for('blocklists'))

# holds definition of general_settings table
general_settings_table = table('general_settings', column('script_enabled'))

@app.route('/power')
def power():
   if url := checkLoggedIn():
      return url

   # get current 'power' state
   query = select([general_settings_table])
   result = mysql_session.execute(query).fetchone()

   script_enabled = result['script_enabled']

   return render_template('power.html', script_enabled=script_enabled)

# post route; changing power to the desired state
@app.route('/power/<desired_state>', methods=['post'])
def changePower(desired_state):
   if url := checkLoggedIn():
      return url

   if desired_state == "enable":
      script_enabled = True
   else:
      script_enabled = False

   mysql_session.execute(general_settings_table.update().values(script_enabled=script_enabled))

   # Commits the changes to the database
   mysql_session.commit()

   return redirect(url_for('power'))

# Runs the flask-application when executing the python script; no need to run "flask" command from command-line
if __name__ == '__main__':
   app.run(debug=True)

