Eyes Unclouded App – Project Summary
Author: Khaylub Thompson-Calvin
Date: April 17, 2025
Course: CIS 234A – Real World Programming
Project: Eyes Unclouded App – Sprint 1

Project Summary – Documentation
This project, 'Eyes Unclouded App', is an interactive Flask + MongoDB system designed for behavioral perception training, emotional awareness logging, and strategic messaging. It replaces previous 'Food Pantry' functionality with a new narrative focused on cognitive mastery and legacy-based learning.
Features

- Role-based Registration & Login
- Hashed passwords with Werkzeug
- Flash messaging and secure session tracking
- Notification (Insight) submission and review
- Date-filtered notification log
- Modular Blueprints for routing
  Functional Areas

1. Account Management
2. Symbolic Notification System
3. Behavioral Data Integration (Atlas DB)
4. Virtue Affinity & Legacy Role Classification
5. Future integration: SQL modeling for traits, insights, and reincarnative timelines.
   🛠️ Technologies

- Flask (Jinja2, Blueprint)
- MongoDB (Local & Atlas)
- HTML5 / CSS3 (custom UI)
- Python 3.11+
  Folder Structure

Assignment1/
├── app.py # Core Flask Application
├── controllers/ # Modular routing logic (auth, notification)
├── documentation/ # Diagrams, notes, and screenshots
├── src/
│ ├── views/
│ │ ├── templates/ # Jinja2 templates for UI
│ │ └── static/ # CSS, JS, and media
├── tests/ # Manual test cases and coverage
└── .env # Future use: hide Mongo URIs and secret keys

What's Next

- Refactor all file names and routes to remove legacy 'food pantry' terms
- Replace static usernames with role-based dashboards (Seeker, Guardian, etc.)
- Add full .env support for secrets and Mongo URIs
- Complete date filtering logic in notification_log
- Convert behavior logs into 'insight chains' for future reincarnation modeling
