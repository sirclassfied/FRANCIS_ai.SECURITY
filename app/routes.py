from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from .models import User, LoginActivity
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import socket
from .ai.detect_anomaly import detect_anomaly
from .email_alerts import send_alert_email
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'danger')
        else:
            new_user = User(username=username, email=email, password=hashed_password, role='user')
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password_input):
            ip = request.remote_addr or socket.gethostbyname(socket.gethostname())
            is_suspicious = detect_anomaly(username, ip)

            login_event = LoginActivity(
                username=username,
                ip_address=ip,
                is_suspicious=is_suspicious
            )
            db.session.add(login_event)
            db.session.commit()

            if is_suspicious:
                send_alert_email(user.email, username, ip)

            session['username'] = user.username
            session['role'] = user.role

            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.user_dashboard'))

        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@main.route('/admin/dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.login'))
    return render_template('admin_dashboard.html')

@main.route('/admin/users')
def manage_users():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('main.login'))
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@main.route('/admin/activity_data')
def activity_data():
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({})
    data = db.session.query(LoginActivity.username, func.count(LoginActivity.id)).group_by(LoginActivity.username).all()
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return jsonify({"labels": labels, "values": values})

@main.route('/user/dashboard')
def user_dashboard():
    if 'role' not in session or session['role'] != 'user':
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.login'))
    return render_template('user_dashboard.html')

@main.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.login'))
