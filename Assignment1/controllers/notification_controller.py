# File: notification_controller.py
# Course: CIS 234A – Real World Programming
# Project: Food Pantry Notification System – Sprint 1
# Author: Khaylub Thompson-Calvin
# Date: 04/14/2025
# Description:
# This module defines the notification controller for the Food Pantry Notification System.
# It is implemented as a Flask Blueprint and provides a test route to verify modular setup.
# Future endpoints related to notification management can be added here for cleaner separation.
#
# Useful Features:
# - Flask Blueprint registered under `/notifications`
# - Isolates notification logic from main app
# - Easily testable via `/notifications/test`
#
# References:
# - Flask Blueprints: https://flask.palletsprojects.com/en/latest/blueprints/
# - PCC CIS234A Course Blueprint Module Notes

from flask import Blueprint, jsonify

# Blueprint Configuration
notification_bp = Blueprint("notification", __name__, url_prefix="/notifications")


# Test Route – Confirms Blueprint is active
@notification_bp.route("/test", methods=["GET"])
def test_notification():
    return jsonify({"message": "Notifications module is working"})
