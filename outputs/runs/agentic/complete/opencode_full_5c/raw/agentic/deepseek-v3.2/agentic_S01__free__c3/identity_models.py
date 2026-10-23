from dataclasses import dataclass
from typing import Optional, Any
from datetime import datetime


@dataclass
class UserRegistrationRequest:
    """Request model for user registration."""

    email: str
    password: str
    name: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class UserRegistrationResponse:
    """Response model for user registration."""

    user_id: str
    email: str
    email_verified: bool
    created_at: Optional[str] = None


@dataclass
class LoginRequest:
    """Request model for user login."""

    email: str
    password: str


@dataclass
class LoginResponse:
    """Response model for user login."""

    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: int
    token_type: str
    user_id: Optional[str] = None
    email: Optional[str] = None


@dataclass
class RefreshRequest:
    """Request model for token refresh."""

    refresh_token: str


@dataclass
class RefreshResponse:
    """Response model for token refresh."""

    access_token: str
    refresh_token: str
    id_token: Optional[str]
    expires_in: int
    token_type: str


@dataclass
class PasswordResetRequest:
    """Request model for password reset."""

    email: str


@dataclass
class PasswordResetResponse:
    """Response model for password reset."""

    success: bool
    message: str


@dataclass
class UserProfile:
    """User profile model."""

    user_id: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    timezone: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class AuthError:
    """Authentication error model."""

    error: str
    error_description: Optional[str] = None
    status_code: Optional[int] = None


def normalize_auth0_user(user_data: dict) -> UserProfile:
    """Normalize Auth0 user data to our UserProfile model."""
    return UserProfile(
        user_id=user_data.get("user_id", ""),
        email=user_data.get("email", ""),
        name=user_data.get("name"),
        picture=user_data.get("picture"),
        locale=user_data.get("locale"),
        timezone=user_data.get("timezone"),
        metadata=user_data.get("user_metadata", {}),
    )


def normalize_login_response(token_data: dict, user_info: dict) -> LoginResponse:
    """Normalize Auth0 login response to our LoginResponse model."""
    return LoginResponse(
        access_token=token_data.get("access_token", ""),
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data.get("expires_in", 0),
        token_type=token_data.get("token_type", ""),
        user_id=user_info.get("sub"),
        email=user_info.get("email"),
    )


def create_error_response(
    error: str, description: str = None, status_code: int = None
) -> AuthError:
    """Create standardized error response."""
    return AuthError(
        error=error, error_description=description, status_code=status_code
    )


def validate_registration_data(
    email: str, password: str, name: str = None
) -> tuple[bool, Optional[str]]:
    """Validate registration data before sending to Auth0."""
    from identity_client import validate_email, validate_password

    if not validate_email(email):
        return False, "Invalid email format"

    is_valid, msg = validate_password(password)
    if not is_valid:
        return False, msg

    if name and len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"

    return True, None
