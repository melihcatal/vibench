from dataclasses import dataclass
from typing import Optional


@dataclass
class UserCredentials:
    email: str
    password: str


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class AuthResponse:
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str
    is_new_user: Optional[bool] = False


@dataclass
class PasswordResetRequest:
    email: str
