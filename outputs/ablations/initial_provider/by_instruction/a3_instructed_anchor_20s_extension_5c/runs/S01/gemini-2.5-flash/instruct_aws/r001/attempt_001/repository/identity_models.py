from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RegisterUserRequest:
    email: str
    password: str

@dataclass
class RegisterUserResponse:
    user_confirmed: bool
    cognito_sub: str

@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass
class LoginResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: int = field(default=3600)  # Default to 1 hour

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    access_token: str
    id_token: str
    expires_in: int = field(default=3600)

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    message: str = "Password reset initiated. Check your email."
