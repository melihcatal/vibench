from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

@dataclass
class RegisterUserResponse:
    uid: str
    email: str
    display_name: Optional[str] = None

@dataclass
class LoginUserRequest:
    email: str
    password: str

@dataclass
class LoginUserResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    local_id: str
    email: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str # Firebase can issue a new refresh token
    expires_in: str
    user_id: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    email: str # Firebase API returns the email on success
