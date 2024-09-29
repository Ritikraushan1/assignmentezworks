# app/utils/email.py
import smtplib
from email.message import EmailMessage
from config import settings
from auth.auth import create_access_token
from datetime import timedelta

def generate_verification_url(user):
    expire = timedelta(hours=1)
    token = create_access_token(data={"sub": user.email}, expires_delta=expire)
    return f"http://localhost:8000/client/verify-email?token={token}"

def send_verification_email(email: str, url: str):
    msg = EmailMessage()
    msg['Subject'] = 'Verify your email'
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = email
    msg.set_content(f'Please verify your email by clicking on the following link: {url}')

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Verification email sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")
