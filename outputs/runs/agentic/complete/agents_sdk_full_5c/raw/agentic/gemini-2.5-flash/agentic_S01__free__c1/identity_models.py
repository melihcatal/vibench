from typing import Optional
from dataclasses import dataclass

@dataclass
class UserRegistrationRequest:
    email: str
    password: str

@dataclass
class UserRegistrationResponse:
    uid: str
    email: str

@dataclass
class UserLoginRequest:
    email: str
    password: str

@dataclass
class UserLoginResponse:
    id_token: str
    refresh_token: str
    expires_in: int

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str
    expires_in: int

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    email: str
