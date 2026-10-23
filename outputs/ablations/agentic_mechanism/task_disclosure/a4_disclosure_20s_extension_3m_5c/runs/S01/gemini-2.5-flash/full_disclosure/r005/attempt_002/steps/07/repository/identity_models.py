from dataclasses import dataclass

@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass
class LoginResponse:
    access_token: str
    refresh_token: str

@dataclass
class RegisterRequest:
    email: str
    password: str
    username: str = None

@dataclass
class RegisterResponse:
    access_token: str
    refresh_token: str

def normalize_email(email: str) -> str:
    """Normalizes an email address to a consistent format (e.g., lowercase)."""
    return email.lower().strip()
