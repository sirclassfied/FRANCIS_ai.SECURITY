# app/email_alerts.py
from flask_mail import Message
from app import mail # CORRECT: Import the globally initialized mail instance from app/__init__.py
# No need for configure_mail function or Mail() instance here.

def send_alert_email(to_email, username, ip):
    try:
        msg = Message(
            subject="🚨 Suspicious Login Detected",
            sender=mail.default_sender, # Use the default sender from config
            recipients=[to_email],
            body=f"Suspicious login detected for user: {username}\nIP Address: {ip}"
        )
        mail.send(msg)
        print(f"✅ Alert email sent to {to_email} for {username}.")
    except Exception as e:
        # Log the actual error for debugging
        print(f"[EMAIL ERROR] Failed to send suspicious login alert to {to_email}: {e}")