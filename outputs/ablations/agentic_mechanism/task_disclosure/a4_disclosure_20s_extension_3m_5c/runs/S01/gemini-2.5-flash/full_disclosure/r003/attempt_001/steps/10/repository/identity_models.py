import dataclasses
import re

@dataclasses.dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str

@dataclasses.dataclass
class EmailPasswordLoginResponse:
    access_token: str
    refresh_token: str

def normalize_email(email: str) -> str:
    """Normalizes an email address to a consistent format."""
    return email.lower().strip()
