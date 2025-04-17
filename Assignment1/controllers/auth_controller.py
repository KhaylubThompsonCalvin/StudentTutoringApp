# File: auth_controller.py
# Course: CIS 234A – Real World Programming
# Project: Eyes Unclouded App – Sprint 1
# Author: Khaylub Thompson-Calvin
# Date: 04/16/2025
# Description:
# Blueprint for authentication logic within Eyes Unclouded App.
# Handles user registration, login, logout, and session flow.
# Designed to support future expansion into virtue-based profiles
# and perceptual learning levels using MongoDB.

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from datetime import datetime


# Blueprint Configuration

# Create the authentication blueprint with URL prefix '/'
auth_bp = Blueprint("auth", __name__, url_prefix="/")


# MongoDB Connection

# Initialize local MongoDB client and select 'eyesUncloudedApp' database
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo["eyesUncloudedApp"]
user_profiles = db["user_profiles"]  # Collection for user profile documents


# Registration Routes

@auth_bp.route("/register", methods=["GET"])
def show_register():
    """
    Display the registration form if not already logged in.
    Redirect to dashboard if session exists.
    """
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Handle registration form submission:
    - Validate matching passwords
    - Hash password and create user document
    - Insert into MongoDB and flash status
    """
    data = request.form
    fullname = data.get("fullname")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for("auth.show_register"))

    user = {
        "fullName": fullname,
        "username": username,
        "email": email,
        "password": generate_password_hash(password),
        "role": "Seeker",
        "learning_level": 1,
        "perception_score": 0,
        "virtue_affinity": [],
        "created_at": datetime.utcnow()
    }

    try:
        user_profiles.insert_one(user)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.show_login"))
    except Exception as e:
        if "E11000" in str(e):
            flash("Username or Email already exists.", "warning")
        else:
            flash(f"Registration failed: {str(e)}", "danger")
        return redirect(url_for("auth.show_register"))


# Login Routes

@auth_bp.route("/login", methods=["GET"])
def show_login():
    """
    Display the login form if not already logged in.
    Redirect to dashboard if session exists.
    """
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Handle login form submission:
    - Verify user exists by username/email
    - Check hashed password
    - Set session variables on success
    """
    data = request.form
    identifier = data.get("identifier")
    password = data.get("password")

    try:
        user = user_profiles.find_one({
            "$or": [{"username": identifier}, {"email": identifier}]
        })

        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Try again.", "danger")
            return redirect(url_for("auth.show_login"))

    except Exception as e:
        flash(f"Login failed: {str(e)}", "danger")
        return redirect(url_for("auth.show_login"))

# --------------------------------
# Logout Route
# --------------------------------
@auth_bp.route("/logout")
def logout():
    """
    Clear user session and redirect to login page.
    """
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.show_login"))
