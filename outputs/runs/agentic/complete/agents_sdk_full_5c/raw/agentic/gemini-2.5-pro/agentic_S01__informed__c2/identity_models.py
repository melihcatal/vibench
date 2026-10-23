# identity_models.py
from dataclasses import dataclass

@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    display_name: str

@dataclass
class User:
    uid: str
    email: str
    display_name: str | None

@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass
class LoginResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    local_id: str

@dataclass
class RefreshRequest:
    refresh_token: str

@dataclass
class RefreshResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    token_type: str
    user_id: str

@dataclass
class PasswordResetRequest:
    email: str
