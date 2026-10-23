from dataclasses import dataclass
from typing import Optional


@dataclass
class RegisterRequest:
    email: str
    password: str


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class ResetRequest:
    email: str


@dataclass
class AuthTokens:
    access_token: str
    id_token: str
    refresh_token: Optional[str]
    expires_in: int
