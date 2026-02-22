from flask_login import login_required, current_user
from flask import render_template, Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        return render_template("admin_dashboard.html")
    elif current_user.role == "doctor":
        return render_template("doctor_dashboard.html")
    elif current_user.role == "nurse":
        return render_template("nurse_dashboard.html")
    else:
        return render_template("patient_dashboard.html")
