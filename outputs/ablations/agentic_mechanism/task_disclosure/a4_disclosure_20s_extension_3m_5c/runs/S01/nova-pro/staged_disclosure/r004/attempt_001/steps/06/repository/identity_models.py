from typing import Dict, Any

class EmailPasswordRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class EmailPasswordResponse:
    def __init__(self, success: bool, message: str, data: Dict[str, Any] = None):
        self.success = success
        self.message = message
        self.data = data or {}

def normalize_email(email: str) -> str:
    return email.lower()

def normalize_password(password: str) -> str:
    return password  # Placeholder for actual password normalization
