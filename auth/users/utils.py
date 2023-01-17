from django.conf import settings
from django.core.mail import send_mail


def send_mail_token(email, token):
    try:
        subject = "welcome to shubham's app"
        message = f'thank you for registering your token is  {token}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        print(f"token successfully send to {recipient_list}")
    except Exception as e:
        return str(e)
