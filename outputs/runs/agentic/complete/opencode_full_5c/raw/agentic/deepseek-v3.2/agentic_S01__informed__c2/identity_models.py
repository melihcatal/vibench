from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    name: Optional[str] = None


@dataclass
class UserRegistrationResponse:
    user_id: str
    email: str
    created_at: str
    provider: str


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class LoginResponse:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: int
    token_type: str
    provider: str


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class RefreshResponse:
    access_token: str
    refresh_token: str
    id_token: Optional[str]
    expires_in: int
    token_type: str
    provider: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    success: bool
    message: str
    provider: str


@dataclass
class UserProfile:
    user_id: str
    email: str
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    email_verified: bool
    created_at: str
    last_login: Optional[str]
    provider: str


@dataclass
class AuthError:
    error: str
    error_description: str
    provider: str


def normalize_auth0_user_response(user_data: Dict[str, Any]) -> UserProfile:
    """Normalize Auth0 user response to our UserProfile model."""
    return UserProfile(
        user_id=user_data.get("user_id", ""),
        email=user_data.get("email", ""),
        name=user_data.get("name"),
        given_name=user_data.get("given_name"),
        family_name=user_data.get("family_name"),
        email_verified=user_data.get("email_verified", False),
        created_at=user_data.get("created_at", ""),
        last_login=user_data.get("last_login"),
        provider="auth0",
    )


def normalize_auth0_token_response(token_data: Dict[str, Any]) -> LoginResponse:
    """Normalize Auth0 token response to our LoginResponse model."""
    return LoginResponse(
        access_token=token_data.get("access_token", ""),
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data.get("expires_in", 0),
        token_type=token_data.get("token_type", ""),
        provider="auth0",
    )
