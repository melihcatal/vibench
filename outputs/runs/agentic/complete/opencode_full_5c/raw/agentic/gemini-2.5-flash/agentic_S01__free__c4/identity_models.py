import dataclasses
from typing import Optional


@dataclasses.dataclass
class RegisterRequest:
    email: str
    password: str
    display_name: Optional[str] = None


@dataclasses.dataclass
class LoginRequest:
    email: str
    password: str


@dataclasses.dataclass
class AuthResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    local_id: str


@dataclasses.dataclass
class PasswordResetRequest:
    email: str


@dataclasses.dataclass
class RefreshTokenRequest:
    refresh_token: str


@dataclasses.dataclass
class RefreshTokenResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    user_id: str
    project_id: str
