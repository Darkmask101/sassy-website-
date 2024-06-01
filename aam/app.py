from flask import Flask, redirect, render_template, request, url_for, flash, session
import pyrebase

Config = {
    "apiKey": "AIzaSyD87hse3yHjHslbS_TIV_3LuCRagaTTqJY",
    "authDomain": "opop-1d92e.firebaseapp.com",
    "databaseURL": "https://opop-1d92e-default-rtdb.firebaseio.com",
    "projectId": "opop-1d92e",
    "storageBucket": "opop-1d92e.appspot.com",
    "messagingSenderId": "787253990360",
    "appId": "1:787253990360:web:f21afd9648acce040ed8ad",
    "measurementId": "G-Q5EKK5WYEL"
}

firebase_app = pyrebase.initialize_app(Config)
db = firebase_app.database()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# In-memory storage for registered users
users = {}

def sanitize_email(email):
    return email.replace('.', ',').replace('@', '_at_')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        sanitized_email = sanitize_email(email)
        users_data = db.child("car").child(sanitized_email).get().val()
        
        # Check if the user is registered and the password matches
        if users_data and users_data.get('name') == name and users_data.get('password') == password:
            session['name'] = name
            return f'<h1>Welcome back, {name}!</h1>'
        else:
            flash('Invalid credentials. Please try again or register.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        reg_name = request.form['name']
        reg_email = request.form['email']
        reg_password = request.form['password']
        
        sanitized_email = sanitize_email(reg_email)
        
        # Check if the email is already registered
        existing_users = db.child("car").get().val()
        if existing_users and sanitized_email in existing_users:
            flash('Email is already registered. Please log in.')
            return redirect(url_for('login'))
        else:
            # Register the user
            new_user = {'name': reg_name, 'password': reg_password}
            db.child("car").child(sanitized_email).set(new_user)
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/greet', methods=['GET', 'POST'])
def greet():
    if 'name' in session:
        name = session['name']
        return f'You have successfully logged in as {name}.'
    return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(debug=True)
