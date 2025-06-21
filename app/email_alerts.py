from flask_mail import Mail, Message

mail = Mail()

def configure_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'          # change this
    app.config['MAIL_PASSWORD'] = 'your_app_password'             # change this
    app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'    # change this
    mail.init_app(app)

def send_alert_email(to_email, username, ip):
    try:
        msg = Message(
            subject="🚨 Suspicious Login Detected",
            recipients=[to_email],
            body=f"Suspicious login detected for user: {username}\nIP Address: {ip}"
        )
        mail.send(msg)
        print("✅ Alert email sent.")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")