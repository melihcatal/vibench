from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class UserRegistrationRequest:
    """Request model for user registration."""

    email: str
    password: str
    display_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UserRegistrationResponse:
    """Response model for user registration."""

    user_id: str
    email: str
    display_name: Optional[str]
    custom_token: str
    provider: str
    created_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class LoginRequest:
    """Request model for user login."""

    email: str
    password: str
    remember_me: bool = False


@dataclass
class LoginResponse:
    """Response model for user login."""

    user_id: str
    email: str
    display_name: Optional[str]
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    provider: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class RefreshRequest:
    """Request model for token refresh."""

    refresh_token: str


@dataclass
class RefreshResponse:
    """Response model for token refresh."""

    user_id: str
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    provider: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class PasswordResetRequest:
    """Request model for password reset."""

    email: str


@dataclass
class PasswordResetResponse:
    """Response model for password reset."""

    email: str
    reset_initiated: bool
    reset_link_sent: bool
    provider: str
    message: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UserProfile:
    """Model for user profile data."""

    user_id: str
    email: str
    display_name: Optional[str]
    email_verified: bool = False
    created_at: Optional[str] = None
    last_login_at: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None


@dataclass
class AuthError:
    """Model for authentication errors."""

    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    provider: Optional[str] = None


def normalize_firebase_user_record(user_record) -> UserProfile:
    """Normalize Firebase user record to UserProfile."""
    return UserProfile(
        user_id=user_record.uid,
        email=user_record.email,
        display_name=user_record.display_name,
        email_verified=user_record.email_verified,
        created_at=user_record.user_metadata.creation_timestamp.isoformat()
        if user_record.user_metadata.creation_timestamp
        else None,
        last_login_at=user_record.user_metadata.last_sign_in_timestamp.isoformat()
        if user_record.user_metadata.last_sign_in_timestamp
        else None,
    )


def normalize_firebase_auth_response(auth_data: Dict[str, Any]) -> LoginResponse:
    """Normalize Firebase auth response to LoginResponse."""
    return LoginResponse(
        user_id=auth_data.get("localId", ""),
        email=auth_data.get("email", ""),
        display_name=auth_data.get("displayName"),
        access_token=auth_data.get("idToken", ""),
        refresh_token=auth_data.get("refreshToken", ""),
        expires_in=auth_data.get("expiresIn", 3600),
        token_type="Bearer",
        provider="firebase",
    )
