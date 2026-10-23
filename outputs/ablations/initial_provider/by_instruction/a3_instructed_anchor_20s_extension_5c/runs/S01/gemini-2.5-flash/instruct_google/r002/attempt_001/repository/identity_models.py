from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RegisterUserRequest:
    email: str
    password: str
    returnSecureToken: bool = True

@dataclass
class LoginUserRequest:
    email: str
    password: str
    returnSecureToken: bool = True

@dataclass
class RefreshTokenRequest:
    grant_type: str = "refresh_token"
    refresh_token: str

@dataclass
class PasswordResetRequest:
    requestType: str = "PASSWORD_RESET"
    email: str

@dataclass
class AuthResponse:
    idToken: str
    email: str
    refreshToken: str
    expiresIn: str
    localId: str
    registered: Optional[bool] = None

@dataclass
class RefreshResponse:
    access_token: str
    expires_in: str
    token_type: str
    refresh_token: str
    id_token: str
    user_id: str
    project_id: str

@dataclass
class PasswordResetResponse:
    email: str
    kind: str
