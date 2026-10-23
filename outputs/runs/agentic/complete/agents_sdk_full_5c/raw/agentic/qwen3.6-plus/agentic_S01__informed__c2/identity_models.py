"""Local request, response, and normalization helpers for Email/Password Account Lifecycle.

Defines data classes for registration, login, session refresh, and password reset
operations, along with utility functions to normalize provider-specific responses
into consistent internal formats.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RegisterRequest:
    """Request payload for creating a new user account."""
    email: str
    password: str
    display_name: Optional[str] = None
    email_verified: bool = False


@dataclass
class RegisterResponse:
    """Response payload after creating a new user account."""
    uid: str
    email: str
    display_name: Optional[str] = None
    email_verified: bool = False
    created_at: Optional[str] = None


@dataclass
class LoginRequest:
    """Request payload for email/password authentication."""
    email: str
    password: str


@dataclass
class LoginResponse:
    """Response payload after successful authentication."""
    id_token: str
    refresh_token: str
    uid: str
    expires_in: int
    email: Optional[str] = None


@dataclass
class RefreshRequest:
    """Request payload for refreshing an access/ID token."""
    refresh_token: str


@dataclass
class RefreshResponse:
    """Response payload after successful token refresh."""
    id_token: str
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"


@dataclass
class PasswordResetRequest:
    """Request payload for initiating a password reset flow."""
    email: str
    continue_url: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class PasswordResetResponse:
    """Response payload after initiating a password reset."""
    email: str


def normalize_register_response(user_record) -> RegisterResponse:
    """Normalize a Firebase UserRecord into a RegisterResponse.

    Args:
        user_record: firebase_admin.auth.UserRecord instance.

    Returns:
        RegisterResponse populated from the user record.
    """
    return RegisterResponse(
        uid=user_record.uid,
        email=user_record.email,
        display_name=user_record.display_name,
        email_verified=user_record.email_verified,
        created_at=user_record.user_metadata.creation_timestamp,
    )


def parse_firebase_id_token_claims(id_token: str) -> dict:
    """Decode and return claims from a Firebase ID token (JWT payload only).

    WARNING: This does NOT verify the signature. Use the Firebase Admin SDK's
    verify_id_token() for production verification. This helper is for
    lightweight client-side inspection only.

    Args:
        id_token: Firebase ID token string.

    Returns:
        Dictionary of JWT payload claims.
    """
    import base64
    import json

    parts = id_token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT token format")

    payload = parts[1]
    # Add padding if needed
    padding = 4 - len(payload) % 4
    if padding != 4:
        payload += "=" * padding

    decoded = base64.urlsafe_b64decode(payload)
    return json.loads(decoded)


def format_login_response_for_frontend(login_response: LoginResponse) -> dict:
    """Format a LoginResponse for safe transmission to a frontend client.

    Omits the refresh_token from the default dict (it should be stored in
    an httpOnly cookie) and presents a clean session object.

    Args:
        login_response: The LoginResponse to format.

    Returns:
        Dictionary suitable for JSON serialization to a frontend.
    """
    return {
        "id_token": login_response.id_token,
        "uid": login_response.uid,
        "expires_in": login_response.expires_in,
        "email": login_response.email,
    }
