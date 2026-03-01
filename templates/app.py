from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models.models import db, User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    @app.route("/")
    def index():
        return render_template("hospital_index.html")

    # Import and register blueprints
    from routes.auth_routes import auth
    from routes.patient_routes import patient
    from routes.appointment_routes import appointment
    from routes.dashboard import dashboard_bp

    # Register blueprints with their URL prefixes
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(patient, url_prefix='/patients')
    app.register_blueprint(appointment, url_prefix='/appointments')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Add additional direct routes for convenience
    @app.route("/login")
    def login_redirect():
        return redirect(url_for('auth.login'))

    @app.route("/register")
    def register_redirect():
        return redirect(url_for('auth.register'))

    @app.route("/dashboard")
    def dashboard_redirect():
        return redirect(url_for('dashboard.dashboard'))

    @app.route("/appointments")
    def appointments_redirect():
        return redirect(url_for('appointment.appointments'))

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
