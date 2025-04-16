from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

# -----------------------------------------------------------------------------  
# Notification Blueprint Setup  
# -----------------------------------------------------------------------------  
# Added `url_prefix='/notifications'` so that all routes will be prefixed properly.
notification_bp = Blueprint('notification', __name__, url_prefix='/notifications')

# -----------------------------------------------------------------------------  
# NEW: Test Route to Validate Blueprint Integration  
# -----------------------------------------------------------------------------  
@notification_bp.route('/test', methods=['GET'])
def test_notification():
    return jsonify({"message": "Notifications module is working"})

# -----------------------------------------------------------------------------  
# Route: Send Notification  
# -----------------------------------------------------------------------------  
@notification_bp.route('/send_notification', methods=['GET', 'POST'])
def send_notification():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # TODO: Add backend logic to send the notification (email, SMS, etc.)
        # TODO: Optionally, record the notification event in the database.

        flash("Notification sent successfully!", "success")
        return redirect(url_for('notification.send_notification'))

    return render_template('send_notification.html')

# -----------------------------------------------------------------------------  
# Route: Create Template  
# -----------------------------------------------------------------------------  
@notification_bp.route('/create_template', methods=['GET', 'POST'])
def create_template():
    if request.method == 'POST':
        template_name = request.form.get('template_name')
        template_subject = request.form.get('template_subject')
        template_body = request.form.get('template_body')

        # TODO: Save the template to the database.

        flash("Template saved successfully!", "success")
        return redirect(url_for('notification.create_template'))

    return render_template('create_template.html')

# -----------------------------------------------------------------------------  
# Route: Notification Log  
# -----------------------------------------------------------------------------  
@notification_bp.route('/notification_log', methods=['GET'])
def notification_log():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    notifications = []

    if start_date and end_date:
        notifications = [
            {
                "subject": "Sample Notification",
                "message": "This is a sample message.",
                "sent_by": "Admin",
                "sent_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "subscriber_count": 100
            }
        ]

    return render_template('notification_log.html', notifications=notifications)


