from flask import Flask,render_template, url_for, request,redirect,flash, session
from werkzeug.security import generate_password_hash, check_password_hash
#from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import config
import requests

app = Flask(__name__)

app.config["SECRET_KEY"] = "you-cannot-hack-it"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'food_securitydb'

mysql = MySQL(app)

msg = ""
suc = ""

# Obtaining weather
def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None
#routing urls
@app.route("/", methods = ['POST','GET'])
def home():
   
   
   
   return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
       
        if check_password_hash(account['password'],password):
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['nat_id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    suc = ''
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'national' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = generate_password_hash(request.form['password']) 
        email = request.form['email']
        national = request.form['national']
        re_password =request.form['re-password']

         # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not check_password_hash(password, re_password):
            msg = 'Password and confirm password doesn\'t match'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s)', (national,username, password, email))
            mysql.connection.commit()
            suc = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg, success = suc)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE nat_id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/covid")
def covid():
     return render_template("covid.html")

@app.route("/records")
def records():
    return render_template("records.html")

@app.route("/farms",  methods=['GET', 'POST'])
def farms():
    msg = ' '
    suc = ' '
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM farm WHERE name = %s', (session['id'],))
        farms = cursor.fetchall()
        # Show the profile page with account info
        

        ## Addding new records
        if request.method == 'POST' and 'farm' in request.form and 'fnum' in request.form:
            farmid = request.form['farm']
            size = request.form["fnum"]
            user = session['id']

            # Check if farm already exists
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM farm WHERE farmID = %s', (farmid,))
            farm = cursor.fetchone()

            if farm:
                msg = "Farm id already exists, try another one"
            else:
                # Farm ID doesnt exists and the form data is valid, now insert new farm records into farm table
                cursor.execute('INSERT INTO farm VALUES (%s, %s, %s)', (farmid,size,user ))
                mysql.connection.commit()
                suc = 'You have successfully registered!'


        return render_template('farm.html', account=farms, msg = msg, suc = suc)
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
@app.route("/crops", methods = ["POST","GET"])
def crops():
    msg = ' '
    suc = ' '
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT farmID FROM farm WHERE name = %s', (session['id'],))
        farms = cursor.fetchall()
        # Show the profile page with account info

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM crop c  INNER JOIN farm f ON c.farmID = f.farmID')
        data = cursor.fetchall()
        
        

        ## Addding new records
        if request.method == 'POST':
            farmid = request.form.get("cfarm")
            cropid = request.form["crop"]
            variety = request.form.get("var")
            name = request.form["cname"].lower()
            date_pur = request.form["pdate"]
            date_plan = request.form["pldate"]
            date_harv = request.form["hdate"]
            price = request.form["price"]
            # Check if crop already exists
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM crop WHERE cropID = %s and name = %s', (cropid,name))
            crop = cursor.fetchone()
            
            

            if crop:
                msg = "Farm id already exists, try another one"
            else:
                # Farm ID doesnt exists and the form data is valid, now insert new farm records into farm table
                cursor.execute('INSERT INTO crop VALUES (%s, %s, %s,%s,%s,%s,%s,%s)', (cropid, variety, name, date_pur, price,farmid,date_plan,date_harv ))
                mysql.connection.commit()
                suc = 'You have successfully added the crop'


        return render_template('crop.html', farm = farms, data=data, msg = msg, suc = suc)
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    


@app.route("/expenses")
def expenses():
    return render_template("expenses.html")

@app.route("/sales")
def sales():
    return render_template("sales.html")




if __name__ == "__main__":
    app.run(debug=True)


