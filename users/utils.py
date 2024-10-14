from cryptography.fernet import Fernet
import base64
from django.conf import settings
from django.core.mail import EmailMessage
import random

def get_encryption_key():
    return settings.SECRET_KEY_ENCRYPTION.encode()

def encrypt_message(message):
    key = get_encryption_key()
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    key = get_encryption_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message.encode()).decode()

def send_email(subject, message, recipient_list):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list
    )
    email.send()

def generate_random_number():
    return random.randint(100000, 999999)

def auth_with_email(user):
    otp = generate_random_number()
    send_email('User Login', f"Your One Time Password is {str(otp)[:3]} {str(otp)[3:]}", [user.email])
    encrypted_otp = encrypt_message(str(otp))
    return {"message": "200", "encrypted_otp": encrypted_otp}
