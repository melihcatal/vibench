"""
Local request, response, and normalization helpers for Email/Password Account Lifecycle.

Provider: Firebase Authentication (referenced for consistency with identity_client.py)
Provider-identifying signals:
  - GOOGLE_APPLICATION_CREDENTIALS references
  - Firebase-specific field naming conventions
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RegisterUserRequest:
    """Request model for creating a new email/password user."""
    email: str
    password: str
    display_name: Optional[str] = None
    email_verified: bool = False
    custom_claims: Optional[Dict[str, Any]] = None


@dataclass
class RegisterUserResponse:
    """Response model after successful user registration."""
    uid: str
    email: str
    display_name: Optional[str]
    email_verified: bool
    disabled: bool
    created_at: Optional[int] = None
    provider: str = "firebase"


@dataclass
class LoginRequest:
    """Request model for email/password authentication."""
    email: str
    password: str


@dataclass
class LoginResponse:
    """Response model after successful login with Firebase Auth."""
    uid: str
    email: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    email_verified: bool = False
    provider: str = "firebase"


@dataclass
class RefreshSessionRequest:
    """Request model for refreshing an expired Firebase session token."""
    refresh_token: str


@dataclass
class RefreshSessionResponse:
    """Response model after successful token refresh."""
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"
    provider: str = "firebase"


@dataclass
class PasswordResetRequest:
    """Request model for initiating a password reset flow."""
    email: str
    continue_url: Optional[str] = None


@dataclass
class PasswordResetResponse:
    """Response model after initiating password reset."""
    email: str
    reset_link: Optional[str] = None
    action_link: Optional[str] = None
    status: str = "initiated"
    provider: str = "firebase"


def build_register_request(**kwargs: Any) -> RegisterUserRequest:
    """Factory for RegisterUserRequest from arbitrary keyword arguments."""
    return RegisterUserRequest(
        email=kwargs.get("email", ""),
        password=kwargs.get("password", ""),
        display_name=kwargs.get("display_name"),
        email_verified=kwargs.get("email_verified", False),
        custom_claims=kwargs.get("custom_claims"),
    )


def build_login_request(**kwargs: Any) -> LoginRequest:
    """Factory for LoginRequest from arbitrary keyword arguments."""
    return LoginRequest(
        email=kwargs.get("email", ""),
        password=kwargs.get("password", ""),
    )


def build_refresh_request(**kwargs: Any) -> RefreshSessionRequest:
    """Factory for RefreshSessionRequest."""
    return RefreshSessionRequest(
        refresh_token=kwargs.get("refresh_token", ""),
    )


def build_password_reset_request(**kwargs: Any) -> PasswordResetRequest:
    """Factory for PasswordResetRequest."""
    return PasswordResetRequest(
        email=kwargs.get("email", ""),
        continue_url=kwargs.get("continue_url"),
    )


def serialize_response(obj: Any) -> Dict[str, Any]:
    """Serialize a dataclass response model into a dictionary."""
    if hasattr(obj, "__dataclass_fields__"):
        return {
            key: getattr(obj, key)
            for key in obj.__dataclass_fields__
        }
    raise TypeError(f"Cannot serialize {type(obj)}")
