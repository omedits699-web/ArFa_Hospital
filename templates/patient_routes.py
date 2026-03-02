from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_required, current_user
from models.models import Patient, db, Appointment
from sqlalchemy.exc import IntegrityError
from datetime import datetime

patient = Blueprint('patient', __name__, url_prefix='/patients')

@patient.route("/")
@login_required
def patient_list():
    """Display all patients with search functionality"""
    search = request.args.get("search", "")
    
    if search:
        patients = Patient.query.filter(
            Patient.name.contains(search) |
            Patient.disease.contains(search)
        ).all()
    else:
        patients = Patient.query.all()
    
    return render_template("patients/list.html", patients=patients, search=search)

@patient.route("/add", methods=["GET", "POST"])
@login_required
def add_patient():
    """Add a new patient"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        disease = request.form.get("disease", "").strip()
        
        # Validation
        if not name:
            flash("Patient name is required", "error")
            return render_template("patients/add.html")
        
        if not age or not age.isdigit() or int(age) <= 0 or int(age) > 150:
            flash("Valid age is required (1-150)", "error")
            return render_template("patients/add.html")
        
        try:
            new_patient = Patient(
                name=name,
                age=int(age),
                disease=disease if disease else "General checkup"
            )
            db.session.add(new_patient)
            db.session.commit()
            flash("Patient added successfully!", "success")
            return redirect(url_for('patient.patient_list'))
        except IntegrityError:
            db.session.rollback()
            flash("Error adding patient. Please try again.", "error")
        except Exception as e:
            db.session.rollback()
            flash("An unexpected error occurred.", "error")
    
    return render_template("patients/add.html")

@patient.route("/<int:patient_id>")
@login_required
def patient_details(patient_id):
    """View patient details"""
    patient = Patient.query.get_or_404(patient_id)
    appointments = Appointment.query.filter_by(patient_name=patient.name).all()
    return render_template("patients/details.html", patient=patient, appointments=appointments)

@patient.route("/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    """Edit patient information"""
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        disease = request.form.get("disease", "").strip()
        
        # Validation
        if not name:
            flash("Patient name is required", "error")
            return render_template("patients/edit.html", patient=patient)
        
        if not age or not age.isdigit() or int(age) <= 0 or int(age) > 150:
            flash("Valid age is required (1-150)", "error")
            return render_template("patients/edit.html", patient=patient)
        
        try:
            patient.name = name
            patient.age = int(age)
            patient.disease = disease if disease else "General checkup"
            db.session.commit()
            flash("Patient information updated successfully!", "success")
            return redirect(url_for('patient.patient_details', patient_id=patient.id))
        except IntegrityError:
            db.session.rollback()
            flash("Error updating patient. Please try again.", "error")
        except Exception as e:
            db.session.rollback()
            flash("An unexpected error occurred.", "error")
    
    return render_template("patients/edit.html", patient=patient)

@patient.route("/<int:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient(patient_id):
    """Delete a patient"""
    patient = Patient.query.get_or_404(patient_id)
    
    try:
        # Check if patient has appointments
        appointments = Appointment.query.filter_by(patient_name=patient.name).all()
        if appointments:
            flash("Cannot delete patient with existing appointments. Please delete appointments first.", "error")
            return redirect(url_for('patient.patient_details', patient_id=patient.id))
        
        db.session.delete(patient)
        db.session.commit()
        flash("Patient deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting patient. Please try again.", "error")
    
    return redirect(url_for('patient.patient_list'))

@patient.route("/api/search")
@login_required
def api_search_patients():
    """API endpoint for patient search (AJAX)"""
    query = request.args.get("q", "")
    
    if len(query) < 2:
        return jsonify([])
    
    patients = Patient.query.filter(
        Patient.name.contains(query)
    ).limit(10).all()
    
    results = []
    for patient in patients:
        results.append({
            'id': patient.id,
            'name': patient.name,
            'age': patient.age,
            'disease': patient.disease
        })
    
    return jsonify(results)

@patient.route("/dashboard")
@login_required
def patient_dashboard():
    """Patient dashboard with statistics"""
    total_patients = Patient.query.count()
    
    # Patients by age groups
    children = Patient.query.filter(Patient.age < 18).count()
    adults = Patient.query.filter(Patient.age.between(18, 60)).count()
    seniors = Patient.query.filter(Patient.age > 60).count()
    
    # Recent patients
    recent_patients = Patient.query.order_by(Patient.id.desc()).limit(5).all()
    
    # Common diseases
    from sqlalchemy import func
    common_diseases = db.session.query(
        Patient.disease,
        func.count(Patient.id).label('count')
    ).group_by(Patient.disease).order_by(func.count(Patient.id).desc()).limit(5).all()
    
    return render_template("patients/dashboard.html", 
                         total_patients=total_patients,
                         children=children,
                         adults=adults,
                         seniors=seniors,
                         recent_patients=recent_patients,
                         common_diseases=common_diseases)
