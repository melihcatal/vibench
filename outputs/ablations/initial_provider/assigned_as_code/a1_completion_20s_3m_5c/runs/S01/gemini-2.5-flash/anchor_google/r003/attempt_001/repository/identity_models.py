from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RegisterUserRequest:
    email: str
    password: str

@dataclass
class RegisterUserResponse:
    user_id: str

@dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str

@dataclass
class EmailPasswordLoginResponse:
    id_token: str
    refresh_token: str
    expires_in: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str
    expires_in: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    message: str
