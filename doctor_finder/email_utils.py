import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_confirmation_email(email):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject='Welcome to Our Site!',
        html_content='<strong>Thank you for registering!</strong>'
    )
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    sg.send(message)
