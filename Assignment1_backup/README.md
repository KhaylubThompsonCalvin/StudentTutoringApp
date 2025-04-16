# Food Pantry Notification System

A real-world Flask + MongoDB app for notifying food-insecure students of available pantry specials.

## Features

- Registration & Login
- Hashed passwords
- Flash messages + session tracking
- Post and view notifications
- Filter notifications by date

## Tested Functionalities

- User authentication (with hashed passwords)
- Flash UI rendering
- Date filtering and session-based access

## Technologies

- Flask
- MongoDB
- Jinja2
- Bootstrap / Custom CSS (optional)

## Developed by

Khaylub Thompson-Calvin | PCC | CIS234A

---

## Project Summary – Documentation

### Project Purpose

In this project, I’m developing a Food Pantry Notification System designed to help a Food Pantry manager communicate more effectively with students facing food insecurity. The system will allow them to send notifications about food availability, specials, or other updates. I’ve started with the foundation account management and I’m building it out iteratively using Agile methodology, sprint by sprint.

---

### What I’ve Built So Far

#### 1. User Account Management

- **Registration**  
  I’ve implemented a user registration endpoint that lets new subscribers sign up with their full name, username, email, and password (plus a password confirmation field). I included logic to make sure both password fields match before creating a new user record in my MongoDB database.  
  Passwords are hashed using Werkzeug for security.

- **Login**  
  For login, I built an endpoint that accepts either a username or email, along with a password. It checks the input against records in the MongoDB collection and returns either a success message or an error if the credentials don’t match. Sessions are tracked using Flask.

---

#### 2. Notifications Module (In Progress)

I’ve scaffolded the notifications module using Flask Blueprints . Right now, it has routes for sending new messages and viewing the notification log. This module will eventually handle:

- Sending broadcast notifications
- Creating reusable message templates
- Storing logs of past messages

---

#### 3. MongoDB Integration

The application is connected to a local MongoDB instance with a dedicated database named `foodPantry`.

- Collections include:

  - `subscribers`
  - `notifications`
  - `templates`
  - `logs`

- I’ve created unique indexes on `username` and `email` fields to prevent duplicate registrations.

---

#### 4. Documentation & Testing

I’m documenting each step of the development process. This includes:

- Clarifying questions
- Implementation notes
- System flow diagrams
- Terminal-based testing using `curl` and `Invoke-RestMethod`
- Markdown and `.txt` files organized under `documentation/` and `tests/`

---

### Project Folder & Path Structure Explained

```plaintext
Assignment1/
│
├── app.py                        # Main Flask application
├── controllers/                 # Modular Flask Blueprints (auth, notifications)
├── documentation/              # Implementation notes, screenshots, diagrams
├── project-backlog/            # Clarifying questions, sprint goals, user stories
├── src/
│   ├── views/
│   │   ├── templates/          # Jinja2 HTML templates
│   │   └── static/             # CSS and JS assets
├── tests/                      # Functional test cases and documentation
└── requirements.txt            # Flask and PyMongo dependencies

```

# Whats Next is I need to Refractor my main Flask application app.py. Also I need to complete test coverage in tests, add enviorment variable loading and .env config and lastly finsh date filter logic in notfication_log.
