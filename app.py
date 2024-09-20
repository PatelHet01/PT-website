from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# app.py (continued)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    dob = db.Column(db.String(10), nullable=False)  # Format: YYYY-MM-DD
    mobile = db.Column(db.String(15), nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


# Home Route
@app.route('/')
def home():
    return render_template('home.html', title='Home')

# About Us Route
@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

# Contact Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        subject = request.form['subject']
        message = request.form['message']
        # Here, you can add logic to save the data or send an email
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact')

# Events Route
@app.route('/events')
def events():
    # Example event data; in a real application, retrieve from a database
    events = [
        {
            'city': 'Mumbai',
            'image': 'images/event1.jpg',
            'title': 'Music Concert',
            'date': '25th September 2024',
            'price': '₹1500'
        },
        {
            'city': 'Delhi',
            'image': 'images/event2.jpg',
            'title': 'Art Exhibition',
            'date': '1st October 2024',
            'price': '₹800'
        },
        # Add more events as needed
    ]
    return render_template('events.html', title='Events', events=events)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        email = request.form['email']
        password = request.form['password']
        # Add authentication logic (e.g., verify against database)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # Add user registration logic (e.g., save to database)
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup')

if __name__ == '__main__':
    app.run(debug=True)
