import dataclasses
from typing import Optional

@dataclasses.dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str

@dataclasses.dataclass
class EmailPasswordLoginResponse:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str

@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

@dataclasses.dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    display_name: Optional[str] = None

@dataclasses.dataclass
class PasswordResetRequest:
    email: str

@dataclasses.dataclass
class PasswordResetResponse:
    message: str

@dataclasses.dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclasses.dataclass
class RefreshSessionResponse:
    access_token: str
    expires_in: int
    token_type: str

def normalize_email(email: str) -> str:
    """Normalizes an email address to a consistent format."""
    return email.lower().strip()

def validate_password_strength(password: str) -> bool:
    """Placeholder for password strength validation."""
    # In a real application, this would include checks for length, complexity, etc.
    return len(password) >= 8
