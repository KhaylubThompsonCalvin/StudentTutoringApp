# File: app.py
# Course: CIS 234A – Real World Programming
# Project: Eyes Unclouded App – Sprint 1
# Author: Khaylub Thompson-Calvin
# Date: 04/16/2025
# Description:
# Implements the web engine for Eyes Unclouded App (Flask + MongoDB).
# Includes splash screen, user registration, login, dashboard, notification posting,
# template creation, and broadcast log filtering.

from datetime import datetime, timedelta
from flask import (
    Flask, request, render_template,
    redirect, url_for, flash, session
)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# ----------------------------------------------------------------------
# Flask App Setup
# ----------------------------------------------------------------------
app = Flask(
    __name__,
    template_folder="src/views/templates",
    static_folder="src/views/static"
)
app.secret_key = "your_secret_key"

# ----------------------------------------------------------------------
# MongoDB Connections
# ----------------------------------------------------------------------
app.config["MONGO_URI"] = "mongodb://localhost:27017/eyesUncloudedApp"
mongo = PyMongo(app)
user_profiles_collection = mongo.db.user_profiles
notifications_collection = mongo.db.notifications

templates_collection = mongo.db.templates

# ----------------------------------------------------------------------
# Authentication Decorator
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
# Routes
# ----------------------------------------------------------------------
@app.route("/splash")
def splash():
    print("[DEBUG] Accessed splash page")
    return render_template("splash.html")

@app.route("/register", methods=["GET", "POST"] )
def show_register():
    print("[DEBUG] Accessed register route")
    if request.method == "POST":
        print("[DEBUG] Received POST data for registration")
        data = request.form
        fullname = data.get("fullname")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirmPassword")
        role = data.get("role")
        learning_level = int(data.get("learning_level"))

        if password != confirm_password:
            print("[ERROR] Passwords do not match.")
            flash("Passwords do not match.", "danger")
            return redirect(url_for("show_register"))

        user = {
            "fullName": fullname,
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "role": role,
            "learning_level": learning_level,
            "perception_score": 0,
            "virtue_affinity": [],
            "created_at": datetime.utcnow()
        }

        try:
            user_profiles_collection.insert_one(user)
            print(f"[DEBUG] Registered user: {username}")
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("show_login"))
        except Exception as e:
            print(f"[ERROR] Registration failed: {e}")
            if "E11000" in str(e):
                flash("Username or Email already exists.", "warning")
            else:
                flash(f"Registration failed: {str(e)}", "danger")
            return redirect(url_for("show_register"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"] )
def show_login():
    print("[DEBUG] Accessed login route")
    if request.method == "POST":
        print("[DEBUG] Received POST data for login")
        identifier = request.form.get("identifier")
        password = request.form.get("password")
        try:
            user = user_profiles_collection.find_one({
                "$or": [{"username": identifier}, {"email": identifier}]
            })
            if user and check_password_hash(user["password"], password):
                print(f"[DEBUG] Login successful for: {identifier}")
                session["user_id"] = str(user["_id"])
                session["username"] = user["username"]
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                print(f"[ERROR] Invalid login for: {identifier}")
                flash("Invalid credentials. Try again.", "danger")
                return redirect(url_for("show_login"))
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            flash(f"Login failed: {str(e)}", "danger")
            return redirect(url_for("show_login"))
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    print(f"[DEBUG] Accessed dashboard for: {session.get('username')}")
    return render_template("dashboard.html", username=session.get("username"))

@app.route("/logout")
def logout():
    print("[DEBUG] Logging out user")
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("show_login"))

@app.route("/notifications", methods=["GET", "POST"])
@login_required
def notifications():
    if request.method == "POST":
        print("[DEBUG] Received POST data for /notifications")
        data = request.form
        note = {
            "title": data.get("title"),
            "message": data.get("message"),
            "virtue_tag": data.get("virtue_tag"),
            "emotion_tag": data.get("emotion_tag"),
            "createdBy": session.get("username"),
            "sent_at": datetime.utcnow()
        }
        try:
            notifications_collection.insert_one(note)
            print("[DEBUG] Notification saved:", note)
            flash("Signal broadcasted successfully.", "success")
        except Exception as e:
            print(f"[ERROR] Failed to broadcast notification: {e}")
            flash(f"Failed to send signal: {str(e)}", "danger")
        return redirect(url_for("notifications"))
    all_notes = list(notifications_collection.find().sort("sent_at", -1))
    print(f"[DEBUG] Fetching {len(all_notes)} notifications")
    return render_template("notifications.html", notifications=all_notes)

@app.route("/create_template", methods=["GET", "POST"])
@login_required
def create_template():
    if request.method == "POST":
        print("[DEBUG] Received POST data for template creation")
        name = request.form.get("template_name")
        subj = request.form.get("template_subject")
        body = request.form.get("template_body")
        if not (name and subj and body):
            flash("All fields are required.", "danger")
        else:
            try:
                templates_collection.insert_one({
                    "name": name,
                    "subject": subj,
                    "body": body,
                    "createdBy": session.get("username"),
                    "created_at": datetime.utcnow()
                })
                print(f"[DEBUG] Template saved: {name}")
                flash("Template saved successfully!", "success")
                return redirect(url_for("create_template"))
            except Exception as e:
                print(f"[ERROR] Template save failed: {e}")
                flash(f"Error saving template: {str(e)}", "danger")
    return render_template("create_template.html")

@app.route("/notification_log", methods=["GET"])
@login_required
def notification_log():
    start = request.args.get("start_date")
    end = request.args.get("end_date")
    query = {}
    if start and end:
        try:
            dt_start = datetime.strptime(start, "%Y-%m-%d")
            dt_end = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
            query["sent_at"] = {"$gte": dt_start, "$lt": dt_end}
        except Exception as e:
            print(f"[ERROR] Date parse failed: {e}")
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")
    notes = list(notifications_collection.find(query).sort("sent_at", -1))
    print(f"[DEBUG] Found {len(notes)} log entries")
    return render_template("notification_log.html", notifications=notes)

@app.route("/")
def index():
    print("[DEBUG] Redirecting to splash")
    return redirect(url_for("splash"))

# ----------------------------------------------------------------------
# Run Server
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("[INFO] Starting EyesUncloudedApp on http://127.0.0.1:7777")
    app.run(port=7777, debug=True)

