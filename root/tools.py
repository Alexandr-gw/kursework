
def get_doctors(db):
    doctors = []
    with db:
        db_doctors = db.fetchAllDoctors()
        for db_doctor in db_doctors:
            doctors.append({'doctor_username': db_doctor.doctor_username,
                            'doctor_password': db_doctor.doctor_password})
    return doctors


def get_patients(db):
    patients = []
    with db:
        db_patients = db.fetchAllPatients()
        for db_patient in db_patients:
            a = db_patient.username
            b = db_patient.patient_password
            patients.append({'username': a, 'patient_password': b})
    return patients
