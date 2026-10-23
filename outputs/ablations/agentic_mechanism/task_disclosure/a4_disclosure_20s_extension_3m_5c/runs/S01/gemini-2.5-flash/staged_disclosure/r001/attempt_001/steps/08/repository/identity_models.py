
import re

class RegistrationRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class RegistrationResponse:
    def __init__(self, user_id, email, message="Registration successful"):
        self.user_id = user_id
        self.email = email
        self.message = message

class LoginRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class LoginResponse:
    def __init__(self, user_id, email, token, message="Login successful"):
        self.user_id = user_id
        self.email = email
        self.token = token
        self.message = message

def normalize_email(email):
    """Normalizes an email address by converting to lowercase and stripping whitespace."""
    if not isinstance(email, str):
        raise TypeError("Email must be a string.")
    return email.strip().lower()

