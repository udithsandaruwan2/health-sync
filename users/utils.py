from cryptography.fernet import Fernet
import base64
from django.conf import settings

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