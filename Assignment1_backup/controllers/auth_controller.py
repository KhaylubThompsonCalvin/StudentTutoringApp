# File: auth_controller.py
# Course: CIS 234A – Real World Programming
# Project: Food Pantry Notification System – Sprint 1
# Author: Khaylub Thompson-Calvin
# Date: 04/14/2025
# Description:
# Handles user authentication routes (register, login, logout) using Flask routes.
# Passwords are hashed using Werkzeug and MongoDB is used for persistence.
# This controller is registered as a Blueprint in app.py.
# References:
# - Flask Documentation: https://flask.palletsprojects.com/
# - MongoDB Atlas: https://www.mongodb.com/docs/
# - Werkzeug Security: https://werkzeug.palletsprojects.com/

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId


# Blueprint Configuration

auth_bp = Blueprint('auth', __name__, url_prefix='/')


# MongoDB Connection

mongo = MongoClient("mongodb://localhost:27017/")
db = mongo['foodPantry']
subscribers_collection = db['subscribers']


# Route: Show Registration Form

@auth_bp.route('/register', methods=['GET'])
def show_register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('register.html')


# Route: Handle Registration Form Submission

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    fullname = data.get('fullname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for('auth.show_register'))

    subscriber = {
        "fullName": fullname,
        "username": username,
        "email": email,
        "password": generate_password_hash(password),
        "role": "subscriber"
    }

    try:
        subscribers_collection.insert_one(subscriber)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.show_login'))
    except Exception as e:
        if "E11000" in str(e):
            flash("Username or Email already exists.", "warning")
        else:
            flash(f"Registration failed: {str(e)}", "danger")
        return redirect(url_for('auth.show_register'))


# Route: Show Login Form

@auth_bp.route('/login', methods=['GET'])
def show_login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Route: Handle Login Form Submission

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    identifier = data.get('identifier')
    password = data.get('password')

    try:
        user = subscribers_collection.find_one({
            "$or": [{"username": identifier}, {"email": identifier}]
        })

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Try again.", "danger")
            return redirect(url_for('auth.show_login'))

    except Exception as e:
        flash(f"Login failed: {str(e)}", "danger")
        return redirect(url_for('auth.show_login'))


# Route: Logout and Clear Session

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.show_login'))
