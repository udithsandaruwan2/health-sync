from cryptography.fernet import Fernet

# Generate a new key
new_key = Fernet.generate_key()
print(new_key.decode())
