from flask import Flask
from flask import request, url_for, render_template, Flask, session
from werkzeug.utils import redirect

app = Flask(__name__)
SECRET_KEY = "Secret key"
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def hello():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'doctor' and request.form['password'] == 'doctor':
            return redirect('/doctor')
        elif request.form['username'] == 'patient' and request.form['password'] == 'patient':
            return redirect('/patient')
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/patient')
def patient():
    return render_template('patient_page.html')


@app.route('create_drug')
def create_drug():
    return render_template('make_drug.html')


@app.route('/doctor')
def doctor():
    return render_template('doctor_page.html')


if __name__ == '__main__':
    app.run(debug=True)
