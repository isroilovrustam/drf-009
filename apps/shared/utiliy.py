import re
import threading
from django.core.mail import EmailMessage
import phonenumbers
from decouple import config
from phonenumbers import NumberParseException
from twilio.rest import Client
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
phone_regex = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")
username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")


# phone_regex = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")

def check_email_or_phone(email_or_phone):
    # Avval email ekanligini tekshiramiz
    if re.fullmatch(email_regex, email_or_phone):
        return "email"

    # Telefon raqam ekanligini tekshiramiz
    try:
        phone_number = phonenumbers.parse(email_or_phone, None)  # Default country code yo'q
        if phonenumbers.is_valid_number(phone_number):
            return "phone"
    except NumberParseException:
        pass  # Xato bo'lsa, davom etamiz

    # Agar email ham, telefon ham bo‘lmasa, xatolik chiqaramiz
    data = {
        "success": False,
        "message": "Email yoki telefon raqamingiz noto‘g‘ri"
    }
    raise ValidationError(data)


def check_user_type(user_input):
    if re.fullmatch(email_regex, user_input):
        return 'email'
    elif re.fullmatch(phone_regex, user_input):
        return 'phone'
    elif re.fullmatch(username_regex, user_input):
        return 'username'
    else:
        raise ValidationError({
            "success": False,
            "message": "Email, username yoki telefon raqamingiz noto'g'ri"
        })


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == "html":
            email.content_subtype = 'html'
        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {"code": code}
    )
    Email.send_email(
        {
            "subject": "Royhatdan otish",
            "to_email": email,
            "body": html_content,
            "content_type": "html"
        }
    )

# def send_phone_code(phone, code):
#     account_sid = config('account_sid')
#     auth_token = config('auth_token')
#     client = Client(account_sid, auth_token)
#     client.messages.create(
#         body=f"Salom do'stim! Sizning tasdiqlash kodingiz: {code}\n",
#         from_="+99899325242",
#         to=f"{phone}"
#     )
