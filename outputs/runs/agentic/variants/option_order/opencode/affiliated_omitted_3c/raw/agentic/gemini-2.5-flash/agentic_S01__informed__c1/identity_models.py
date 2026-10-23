import dataclasses
from typing import Optional


@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class RegisterUserResponse:
    _id: str
    email: str
    email_verified: bool


@dataclasses.dataclass
class LoginRequest:
    username: str
    password: str
    audience: str
    scope: str
    client_id: str
    grant_type: str = "http://auth0.com/oauth/token"


@dataclasses.dataclass
class LoginResponse:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: str
    token_type: str
    expires_in: int


@dataclasses.dataclass
class RefreshTokenRequest:
    grant_type: str
    client_id: str
    refresh_token: str


@dataclasses.dataclass
class RefreshTokenResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int


@dataclasses.dataclass
class PasswordResetRequest:
    email: str
    connection: str
    client_id: str


@dataclasses.dataclass
class PasswordResetResponse:
    message: str
