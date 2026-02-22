from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models.models import User, db
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = "patient"  # All registered users are patients by default

        # Validation
        if not username or not password:
            return render_template("register.html", error="Username and password are required")
        
        if len(username) < 3:
            return render_template("register.html", error="Username must be at least 3 characters long")
        
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters long")
        
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("register.html", error="Username already exists")

        try:
            new_user = User(username=username, role=role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/auth/login")
        except IntegrityError:
            db.session.rollback()
            return render_template("register.html", error="Username already exists")
        except Exception as e:
            db.session.rollback()
            return render_template("register.html", error="Registration failed. Please try again.")

    return render_template("register.html")

@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect("/dashboard")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/auth/login")
