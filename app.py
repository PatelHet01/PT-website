from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title="Home")

@app.route('/about')
def about():
    return render_template('aboutus.html', title="About Us")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact")

@app.route('/events')
def events():
    return render_template('events.html', title="Events")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        email = request.form['email']
        password = request.form['password']
        # Add authentication logic
        return redirect(url_for('home'))
    return render_template('login.html', title="Login")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here
        email = request.form['email']
        password = request.form['password']
        # Add user registration logic
        return redirect(url_for('login'))
    return render_template('signup.html', title="Signup")

if __name__ == '__main__':
    app.run(debug=True)
