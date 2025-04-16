# File: app.py
# Course: CIS 234A – Real World Programming
# Project: Food Pantry Notification System – Sprint 1
# Author: Khaylub Thompson-Calvin
# Date: 04/14/2025
# Description:
# This module implements the core web interface for the Food Pantry Notification System using Flask.
# It includes user registration, login, session management, and CRUD operations for posting
# notifications, managing templates, and viewing logs. Authentication is enforced using
# session cookies and login decorators. MongoDB is used for all backend data storage,
# including subscribers, notifications, and templates.
#
# Useful Features:
# - Login with username or email (flexible identifier)
# - Password hashing with Werkzeug
# - Flash messaging for status alerts
# - Flask Blueprint support for modular controllers
# - Notification posting & filtering
# - Template creation for reusable messages
# - Log viewing with date-based filtering
#
# References:
# - Flask Documentation: https://flask.palletsprojects.com/
# - MongoDB Python Driver (PyMongo): https://pymongo.readthedocs.io/
# - Werkzeug Security: https://werkzeug.palletsprojects.com/
# - PCC CIS234A Course Materials


import sys
import os
from datetime import datetime, timedelta
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    flash,
    redirect,
    url_for,
    session,
)
from flask_pymongo import PyMongo
from controllers.notification_controller import notification_bp
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# ----------------------------------------------------------------------
# Flask App Initialization
# ----------------------------------------------------------------------
app = Flask(
    __name__,
    template_folder="src/views/templates",
    static_folder="src/views/static",  # Optional, ensure folder exists or remove
)
app.secret_key = "your_secret_key"

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/foodPantry"
mongo = PyMongo(app)
subscribers_collection = mongo.db.subscribers

# Register Blueprint
app.register_blueprint(notification_bp)


# ----------------------------------------------------------------------
# Login Required Decorator
# ----------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Login required.", "warning")
            return redirect(url_for("show_login"))
        return f(*args, **kwargs)

    return decorated_function


# ----------------------------------------------------------------------
# Registration Routes
# ----------------------------------------------------------------------
@app.route("/register", methods=["GET"])
def show_register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.form
    fullname = data.get("fullname")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for("show_register"))

    subscriber = {
        "fullName": fullname,
        "username": username,
        "email": email,
        "password": generate_password_hash(password),
        "role": "subscriber",
    }

    try:
        subscribers_collection.insert_one(subscriber)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("show_login"))
    except Exception as e:
        if "E11000" in str(e):
            flash("Username or Email already exists.", "warning")
        else:
            flash(f"Registration failed: {str(e)}", "danger")
        return redirect(url_for("show_register"))


# ----------------------------------------------------------------------
# Login Routes
# ----------------------------------------------------------------------
@app.route("/login", methods=["GET"])
def show_login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.form
    identifier = data.get("identifier")
    password = data.get("password")

    try:
        user = subscribers_collection.find_one(
            {"$or": [{"username": identifier}, {"email": identifier}]}
        )

        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Try again.", "danger")
            return redirect(url_for("show_login"))

    except Exception as e:
        flash(f"Login failed: {str(e)}", "danger")
        return redirect(url_for("show_login"))


# ----------------------------------------------------------------------
# Dashboard
# ----------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session.get("username"))


# ----------------------------------------------------------------------
# Notifications
# ----------------------------------------------------------------------
@app.route("/notifications", methods=["GET", "POST"])
@login_required
def notifications():
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")

        if not title or not message:
            flash("Both title and message are required.", "danger")
        else:
            mongo.db.notifications.insert_one(
                {
                    "title": title,
                    "message": message,
                    "createdBy": session.get("username"),
                    "sent_at": datetime.utcnow(),
                }
            )
            flash("Notification created successfully!", "success")

    all_notifications = list(mongo.db.notifications.find())
    return render_template(
        "notifications.html",
        notifications=all_notifications,
        username=session.get("username"),
    )


# Create Template Route


@app.route("/create_template", methods=["GET", "POST"])
@login_required
def create_template():
    if request.method == "POST":
        template_name = request.form.get("template_name")
        template_subject = request.form.get("template_subject")
        template_body = request.form.get("template_body")

        if not template_name or not template_subject or not template_body:
            flash("All fields are required.", "danger")
        else:
            try:
                mongo.db.templates.insert_one(
                    {
                        "name": template_name,
                        "subject": template_subject,
                        "body": template_body,
                        "createdBy": session.get("username"),
                        "created_at": datetime.utcnow(),
                    }
                )
                flash("Template saved successfully!", "success")
                return redirect(url_for("create_template"))
            except Exception as e:
                flash(f"Error saving template: {str(e)}", "danger")

    return render_template("create_template.html")


# Notification Log


@app.route("/notification_log", methods=["GET"])
@login_required
def notification_log():
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    query = {}
    if start_date_str and end_date_str:
        try:
            start = datetime.strptime(start_date_str, "%Y-%m-%d")
            end = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)
            query["sent_at"] = {"$gte": start, "$lt": end}
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")

    notifications = list(mongo.db.notifications.find(query))
    return render_template("notification_log.html", notifications=notifications)


# Logout


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("show_login"))


# Home


@app.route("/")
def index():
    return render_template("splash.html")


# Run the app

if __name__ == "__main__":
    app.run(port=5001, debug=True)
