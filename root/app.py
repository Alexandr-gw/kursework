from flask import request, url_for, render_template, Flask, session
from werkzeug.utils import redirect

from root.db import Database
from root.entities import Symptom, Contraindication, Drug, Doctor, Patient
from root.tools import get_patients, get_doctors, checkValues, handle_extra_info, validate_doctor, validate_patient

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
        username = request.form['username']
        password = request.form['password']
        if user_type == 'patient':
            patients = get_patients(db)
            for patient in patients:
                if patient['username'] == username and patient['patient_password'] == password:
                    session['username'] = username
                    return redirect('/patient')
            error = 'There is no patient with this credentials'
        elif user_type == 'doctor':
            doctors = get_doctors(db)
            for doctor in doctors:
                if doctor['doctor_username'] == username and doctor['doctor_password'] == password:
                    session['username'] = username
                    return redirect('/doctor')
            error = 'There is no doctor with this credentials'
    return render_template('login.html', error=error)


@app.route('/patient')
def patient():
    username = session.get('username')
    with db:
        all_symptoms = db.fetchAllSymptoms()
        all_contraindications = db.fetchAllContraindications()
        return render_template('patient_page.html', username=username, symptoms=all_symptoms,
                               contras=all_contraindications)


@app.route('/create_drug', methods=['GET', 'POST'])
def create_drug():
    error = None
    if request.method == 'POST':
        drug = request.form['drug_name']
        symptom = request.form['symptom']
        contra = request.form['contra']
        price = request.form['price']
        extra_info = handle_extra_info(request.form['extra_contra'])

        error = checkValues(drug, symptom, contra, price)
        if not error:
            db_symptom = Symptom(symptom_name=symptom)
            db_contra = Contraindication(name=contra, additional_info=extra_info)
            db_drug = Drug(drug_name=drug, price=price, symptom_name=symptom, contraindication=contra)
            with db:
                db.createSymptom(db_symptom)
                db.createContraindication(db_contra)
                db.createDrug(db_drug)
            return redirect('/doctor')
    return render_template('make_drug.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/doctor')
def doctor():
    with db:
        drugs = db.fetchAllDrugs()
        return render_template('doctor_page.html', drugs=drugs, username=session.get('username'))


@app.route('/show_drugs', methods=['GET', 'POST'])
def show_drugs():
    if request.method == 'POST':
        symp = request.form.getlist('symptom_list')
        contr = request.form.getlist('contras_list')
    return render_template('no_drugs_page.html', username=session.get('username'))


@app.route('/signup_patient', methods=['GET', 'POST'])
def signup_patient():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        password1 = request.form['password1']
        error = validate_patient(username, name, surname, password, password1)
        if not error:
            with db:
                patient = Patient(username=username, name=name, surname=surname, patient_password=password)
                db.createPatient(patient)
    return render_template('signup_patient.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        password1 = request.form['password1']
        error = validate_doctor(username, name, surname, password, password1)
        if not error:
            with db:
                doctor = Doctor(doctor_username=username, name=name,
                                surname=str(surname), doctor_password=password)
                db.createDoctor(doctor)

    return render_template('signup.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
