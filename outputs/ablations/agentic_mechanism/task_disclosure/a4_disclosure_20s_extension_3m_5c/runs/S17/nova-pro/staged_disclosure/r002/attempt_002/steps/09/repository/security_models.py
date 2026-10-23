from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())


def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()


def normalize_response(response):
    # Placeholder for response normalization logic
    return response