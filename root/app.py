from flask import Flask

app = Flask(__name__)
SECRET_KEY = "Secret key"
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def hello():
    return
