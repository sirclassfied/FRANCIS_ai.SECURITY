# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db, mail # Import db and mail from app's __init__.py
from app.models import User, LoginActivity # Correctly import models
from flask_login import login_user, logout_user, login_required, current_user # Flask-Login functions/decorators

from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message # For sending emails in password reset

import socket # Assuming you still need this for IP address
from app.ai.detect_anomaly import detect_anomaly # Your AI anomaly detection function
from app.email_alerts import send_alert_email # Your email alert function

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # current_user is provided by Flask-Login and works whether logged in or not
    if current_user.is_authenticated:
        return render_template('home.html', user=current_user)
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # Prevent logged-in users from registering again
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([username, email, password]):
            flash('All fields are required!', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # If already logged in, redirect
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username_input = request.form.get('username')
        password_input = request.form.get('password')

        user = User.query.filter_by(username=username_input).first()

        if user and check_password_hash(user.password, password_input):
            # Log the user in with Flask-Login. 'remember=True' keeps them logged in.
            login_user(user, remember=True)
            flash('Login successful!', 'success')

            # Log activity
            ip = request.remote_addr
            is_suspicious = detect_anomaly(username_input, ip)

            new_activity = LoginActivity(username=username_input, ip_address=ip, is_suspicious=is_suspicious)
            db.session.add(new_activity)
            db.session.commit()

            if is_suspicious:
                send_alert_email(user.email, user.username, ip)
                flash('Suspicious login detected and alert sent!', 'warning')

            # Redirect to the 'next' page if it was set (e.g., from an @login_required redirect)
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page or url_for('main.admin_dashboard'))
            else:
                return redirect(next_page or url_for('main.user_dashboard'))
        else:
            flash('Login failed. Check username and password.', 'danger')
    return render_template('login.html')

@main.route('/logout')
@login_required # Ensure only logged-in users can logout
def logout():
    logout_user() # Log the user out with Flask-Login
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home')) # Redirect to home or login page


# Password Reset Request Route
@main.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated: # Don't allow if already logged in
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Send reset email
            token = user.get_reset_token()
            msg = Message(
                subject="Password Reset Request for Your FRANCIS_IA Account",
                sender=mail.default_sender, # Use the default sender configured in app/__init__.py
                recipients=[user.email]
            )
            # IMPORTANT: Create a proper HTML template for this email in production!
            # For simplicity, using plain text here.
            msg.body = f'''To reset your password, visit the following link:
{url_for('main.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
            try:
                mail.send(msg)
                flash('An email has been sent with instructions to reset your password.', 'info')
            except Exception as e:
                # Log the actual error for debugging, but show generic message to user
                print(f"Error sending password reset email: {e}")
                flash('Failed to send password reset email. Please try again later.', 'danger')
        else:
            # For security, always show a generic message if email not found
            flash('If an account with that email exists, an email has been sent.', 'info')
        return redirect(url_for('main.login')) # Always redirect to login to prevent email harvesting

    return render_template('reset_password_request.html') # Create this template


# Reset Password Route (with token)
@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated: # Don't allow if already logged in
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('main.reset_password_request'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You are now able to log in.', 'success')
            return redirect(url_for('main.login'))

    return render_template('reset_token.html') # Create this template


# Protected Dashboards
@main.route('/admin_dashboard')
@login_required # Protect this route: requires login
def admin_dashboard():
    if not current_user.is_admin: # Additional check for admin role
        flash('Access denied: You do not have admin privileges.', 'danger')
        return redirect(url_for('main.user_dashboard')) # Redirect to user dashboard if not admin
    return render_template('admin_dashboard.html', user=current_user)

@main.route('/user_dashboard')
@login_required # Protect this route: requires login
def user_dashboard():
    return render_template('user_dashboard.html', user=current_user)

# Error Handlers (Good Practice)
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# You can add more error handlers as needed, e.g., for 500 Internal Server Error
# @main.app_errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500