from flask import Flask, render_template, request, redirect, send_file
from models import Session, Owner, Patient, MedicalHistory, init_db
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

init_db()

# connect to database
session = Session()
from models import Session, Owner, Patient, MedicalHistory
@app.route('/')
def home():
    return render_template('form.html')
@app.route('/submit', methods=['POST'])
def submit():
    owner = Owner(
        name=request.form['owner'],
        phone=request.form['phone'],
        email=request.form.get('email'),
        address=request.form.get('address')
    )

    patient = Patient(
        name=request.form['pet'],
        species=request.form['species'],
        breed=request.form['breed'],
        age=request.form.get('age'),
        sex=request.form.get('sex'),
        weight=request.form.get('weight'),
        owner=owner
    )

    vaccines_list = request.form.getlist('vaccines')
    vaccines_text = ", ".join(vaccines_list)

    history = MedicalHistory(
        medications=request.form.get('medications'),
        allergies=request.form.get('allergies'),
        past_history=request.form.get('history'),
        diet=request.form.get('diet'),
        reason=request.form.get('reason'),
        notes=request.form.get('notes'),
        
        # Vitals
        weight=request.form.get('weight'),
        temperature=request.form.get('temperature'),
        heart_rate=request.form.get('heart_rate'),
        respiratory_rate=request.form.get('respiratory_rate'),

        # FAS
        fas_score=request.form.get('fas_score'),
        fas_notes=request.form.get('fas_notes'),

        reproductive_status=request.form.get('reproductive_status'),
        vaccines=vaccines_text,

        integument=request.form.get('integument'),
        ent=request.form.get('ent'),
        msk=request.form.get('msk'),
        lymph_nodes=request.form.get('lymph_nodes'),
        cardiovascular=request.form.get('cardiovascular'),
        respiratory=request.form.get('respiratory'),
        gastrointestinal=request.form.get('gastrointestinal'),
        neurologic=request.form.get('neurologic'),

        date=None,
        patient=patient
    )

    session.add(owner)
    session.add(patient)
    session.add(history)
    session.commit()

    return redirect('/search')
@app.route('/search')
def search():
    query = request.args.get('q', '')

    results = session.query(Patient).join(Owner).filter(
        (Patient.name.contains(query)) |
        (Owner.name.contains(query)) |
        (Owner.phone.contains(query))
    ).all()

    return render_template('search.html', results=results)
@app.route('/pdf/<int:patient_id>')
def generate_pdf(patient_id):
    patient = session.query(Patient).get(patient_id)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 800, f"Patient: {patient.name}")
    pdf.drawString(100, 780, f"Owner: {patient.owner.name}")
    pdf.drawString(100, 760, f"Phone: {patient.owner.phone}")

    y = 720
    for h in patient.histories:
        pdf.drawString(100, y, f"- {h.notes}")
        y -= 20

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="record.pdf")
@app.route('/patient/<int:patient_id>')
def view_patient(patient_id):
    patient = session.query(Patient).get(patient_id)
    return render_template('patient.html', patient=patient)

@app.route('/edit/<int:history_id>', methods=['GET', 'POST'])
def edit_visit(history_id):
    history = session.query(MedicalHistory).get(history_id)

    if request.method == 'POST':
        history.weight = request.form.get('weight')
        history.temperature = request.form.get('temperature')
        history.heart_rate = request.form.get('heart_rate')
        history.respiratory_rate = request.form.get('respiratory_rate')

        history.fas_score = request.form.get('fas_score')
        history.fas_notes = request.form.get('fas_notes')

        history.medications = request.form.get('medications') # type: ignore
        history.allergies = request.form.get('allergies')
        history.past_history = request.form.get('history')
        history.diet = request.form.get('diet')
        history.reason = request.form.get('reason')
        history.vaccines = request.form.get('vaccines')

        history.integument = request.form.get('integument')
        history.ent = request.form.get('ent')
        history.msk = request.form.get('msk')
        history.lymph_nodes = request.form.get('lymph_nodes')
        history.cardiovascular = request.form.get('cardiovascular')
        history.respiratory = request.form.get('respiratory')
        history.gastrointestinal = request.form.get('gastrointestinal')
        history.neurologic = request.form.get('neurologic')

        history.notes = request.form.get('notes')

        session.commit()
        return redirect(f'/patient/{history.patient_id}')

    return render_template('edit.html', history=history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    