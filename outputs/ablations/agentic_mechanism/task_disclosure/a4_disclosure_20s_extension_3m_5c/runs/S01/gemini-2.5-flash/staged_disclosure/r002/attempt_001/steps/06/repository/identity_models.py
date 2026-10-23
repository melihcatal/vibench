from dataclasses import dataclass

@dataclass
class EmailPasswordSignUpRequest:
    email: str
    password: str

@dataclass
class EmailPasswordSignInRequest:
    email: str
    password: str

@dataclass
class EmailPasswordResponse:
    user_id: str
    message: str = "Success"

def normalize_email(email: str) -> str:
    """Normalizes an email address to a canonical format."""
    return email.lower().strip()
