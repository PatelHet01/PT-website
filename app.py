from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import re
from flask_mail import Mail, Message

app = Flask(__name__)

# Secret key for session management. It should be a random string.
app.secret_key = 'Het@123456'

# Set the path for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hackair/pt/privent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize the database and create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')

# Route for hosting an event
@app.route('/host', methods=['GET'])
def host():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    return render_template('host.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validate the password
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message)  # Flash the validation message
            return redirect(url_for('signup'))  # Redirect back to signup page

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Redirect to login page after signup

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the database for the user
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in session
            session['user_email'] = user.email  # Store email for user info display
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
    return render_template('dashboard.html')  # Use your dashboard template

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, "Password is valid."

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    session.pop('user_email', None)  # Remove user email from session
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))  # Redirect to the login page

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        # Generate a reset token (implement your token generation logic)
        token = generate_reset_token(email)  # Implement this function

        # Create the reset link
        reset_link = url_for('reset_password', token=token, _external=True)

        # Send the email
        msg = Message('Password Reset Request', recipients=[email])
        msg.body = f'Click the link to reset your password: {reset_link}'
        mail.send(msg)

        flash('If your email is registered, you will receive a password reset link.', 'info')
        return redirect(url_for('login'))

    return render_template('forgot_password.html')

app.config['MAIL_SERVER'] = 'smtp.example.com'  # Your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

mail = Mail(app)


if __name__ == '__main__':
    app.run(debug=True)
