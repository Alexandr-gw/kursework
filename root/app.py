from flask import request, url_for, render_template, Flask, session
from werkzeug.utils import redirect

from root.db import Database
from root.tools import get_patients, get_doctors

app = Flask(__name__)
SECRET_KEY = "Secret key"
app.config['SECRET_KEY'] = SECRET_KEY

db = Database()
app.config['SQLALCHEMY_DATABASE_URI'] = db.cstr


@app.route('/')
def hello():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_type = request.form['exampleRadios']
        username =  request.form['username']
        password = request.form['password']
        if user_type == 'patient':
            patients = get_patients(db)
            for patient in patients:
                if patient['username'] == username and patient['patient_password'] == password:
                    return redirect('/patient')
            error = 'There is no patient with this credentials'
        elif user_type == 'doctor':
            doctors = get_doctors(db)
            for doctor in doctors:
                if doctor['doctor_username'] == username and doctor['doctor_password'] == password:
                    return redirect('/doctor')
            error = 'There is no doctor with this credentials'
    return render_template('login.html', error=error)


@app.route('/patient')
def patient():
    return render_template('patient_page.html')


@app.route('/create_drug')
def create_drug():
    return render_template('make_drug.html')


@app.route('/logout')
def logout():
    return "logged out"


@app.route('/doctor')
def doctor():
    return render_template('doctor_page.html')


if __name__ == '__main__':
    app.run(debug=True)
