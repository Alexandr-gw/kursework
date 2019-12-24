from flask import Flask
from flask import request, url_for, render_template, Flask, session

app = Flask(__name__)
SECRET_KEY = "Secret key"
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def hello():
    return render_template('start_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "Logged in"
    return "Here"


if __name__ == '__main__':
    app.run(debug=True)
