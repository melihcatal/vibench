"""Define local request, response, and normalization helpers for Email/Password Account Lifecycle."""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class LoginRequest:
    """Request model for login operations."""

    email: str
    password: str
    scope: Optional[str] = "openid profile email"


@dataclass
class LoginResponse:
    """Response model for login operations."""

    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: int
    token_type: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "id_token": self.id_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
        }


@dataclass
class RefreshResponse:
    """Response model for refresh operations."""

    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: int
    token_type: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "id_token": self.id_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
        }


@dataclass
class UserRegistration:
    """Model for user registration."""

    email: str
    password: str
    name: Optional[str] = None
    user_metadata: Optional[Dict[str, Any]] = None

    def validate(self) -> tuple[bool, str]:
        """Validate registration data."""
        from identity_client import validate_email, validate_password

        if not validate_email(self.email):
            return False, "Invalid email format"

        is_valid, message = validate_password(self.password)
        if not is_valid:
            return False, message

        return True, "Valid"


@dataclass
class PasswordResetRequest:
    """Model for password reset requests."""

    email: str
    connection: str = "Username-Password-Authentication"


def normalize_auth0_error(error: Exception) -> str:
    """Normalize Auth0 error messages."""
    error_str = str(error)

    if "invalid_grant" in error_str:
        return "Invalid email or password"
    elif "too many requests" in error_str:
        return "Too many login attempts. Please try again later."
    elif "invalid_request" in error_str:
        return "Invalid request. Please check your input."
    elif "access_denied" in error_str:
        return "Access denied. Please contact support."
    else:
        return f"Authentication error: {error_str}"
