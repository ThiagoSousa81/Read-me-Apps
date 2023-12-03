from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!<br>HTTP: 200 OK'

@app.route('/about')
def about():
    return 'About'
