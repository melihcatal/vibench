"""
identity_models.py
Local request, response, and normalization helpers for Email/Password Account Lifecycle.

Defines dataclasses for requests and responses across registration,
login, token refresh, and password reset flows.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# ---- Registration ----


@dataclass
class RegistrationRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    locale: Optional[str] = "en-US"


@dataclass
class RegistrationResponse:
    uid: str
    email: str
    display_name: Optional[str] = None
    email_verified: bool = False
    created_at: Optional[int] = None


# ---- Login ----


@dataclass
class LoginRequest:
    email: str
    password: str
    mfa_token: Optional[str] = None


@dataclass
class LoginResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 3600
    scope: Optional[str] = None


# ---- Token Refresh ----


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class RefreshResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 86400
    scope: Optional[str] = None


# ---- Password Reset ----


@dataclass
class PasswordResetRequest:
    email: str
    redirect_url: Optional[str] = None


@dataclass
class PasswordResetResponse:
    success: bool
    email: str
    message: str
    cloud_directory_user_id: Optional[str] = None


# ---- Normalization helpers ----


def normalize_email(email: str) -> str:
    """Normalize email address to lowercase, stripped whitespace."""
    if not email:
        raise ValueError("Email address is required.")
    return email.strip().lower()


def validate_password_strength(password: str) -> bool:
    """
    Basic password strength validation:
    - At least 8 characters
    - Contains uppercase, lowercase, digit, and special character
    """
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    return has_upper and has_lower and has_digit and has_special


def build_user_metadata(
    uid: str,
    email: str,
    display_name: Optional[str] = None,
    locale: Optional[str] = None,
) -> dict:
    """Build a normalized user metadata dictionary."""
    metadata = {
        "uid": uid,
        "email": email,
        "display_name": display_name or email.split("@")[0],
        "locale": locale or "en-US",
        "created_at": datetime.utcnow().isoformat(),
    }
    return metadata
