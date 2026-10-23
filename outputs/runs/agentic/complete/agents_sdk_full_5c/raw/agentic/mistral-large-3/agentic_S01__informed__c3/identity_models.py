from typing import Dict, Optional, TypedDict
from dataclasses import dataclass


class RegisterUserRequest(TypedDict):
    email: str
    password: str
    given_name: Optional[str]
    family_name: Optional[str]


class RegisterUserResponse(TypedDict):
    user_id: str
    email_verified: bool
    status: str


class LoginRequest(TypedDict):
    email: str
    password: str


class LoginResponse(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
    id_token: Optional[str]


class RefreshSessionRequest(TypedDict):
    refresh_token: str


class RefreshSessionResponse(TypedDict):
    access_token: str
    expires_in: int
    id_token: Optional[str]


class PasswordResetRequest(TypedDict):
    email: str


class PasswordResetResponse(TypedDict):
    status: str
    reset_sent: bool


@dataclass
class Auth0User:
    user_id: str
    email: str
    email_verified: bool
    given_name: Optional[str] = None
    family_name: Optional[str] = None


@dataclass
class Auth0TokenResponse:
    access_token: str
    refresh_token: str
    expires_in: int
    id_token: Optional[str] = None
    token_type: str = "Bearer"