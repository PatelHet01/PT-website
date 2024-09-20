from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/host')
def host():
    return render_template('host.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
