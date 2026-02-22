from flask import Blueprint, render_template, request
from flask_login import login_required
from models.models import Appointment, db

appointment = Blueprint('appointment', __name__, url_prefix='/appointments')

@appointment.route("/")
@login_required
def appointments():
    search = request.args.get("search")

    if search:
        results = Appointment.query.filter(
            Appointment.patient_name.contains(search)
        ).all()
    else:
        results = Appointment.query.all()

    return render_template("appointments.html", data=results)
