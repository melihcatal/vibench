from dataclasses import dataclass
from typing import Optional


@dataclass
class UserRecord:
    uid: str
    email: Optional[str] = None
    display_name: Optional[str] = None


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class LoginResponse:
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class RefreshResponse:
    id_token: str
    refresh_token: str
    expires_in: int
    user_id: str
