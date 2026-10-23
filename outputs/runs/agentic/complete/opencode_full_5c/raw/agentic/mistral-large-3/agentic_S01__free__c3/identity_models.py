from typing import Dict, Any, Optional, TypedDict
from dataclasses import dataclass


class UserRegistrationRequest(TypedDict):
    """Request model for user registration."""

    email: str
    password: str
    display_name: Optional[str]
    metadata: Optional[Dict[str, Any]]


class UserRegistrationResponse(TypedDict):
    """Response model for user registration."""

    user_id: str
    email: str
    display_name: Optional[str]
    provider: str
    provider_response: Dict[str, Any]


class LoginRequest(TypedDict):
    """Request model for email/password login."""

    email: str
    password: str


class LoginResponse(TypedDict):
    """Response model for email/password login."""

    access_token: str
    refresh_token: Optional[str]
    expires_in: int
    user_info: Dict[str, Any]
    provider: str


class RefreshSessionRequest(TypedDict):
    """Request model for session refresh."""

    refresh_token: str


class RefreshSessionResponse(TypedDict):
    """Response model for session refresh."""

    access_token: str
    expires_in: int
    token_type: str
    scope: Optional[str]
    provider: str


class PasswordResetRequest(TypedDict):
    """Request model for password reset."""

    email: str


class PasswordResetResponse(TypedDict):
    """Response model for password reset initiation."""

    delivery_details: Dict[str, Any]
    provider: str
    status: str


@dataclass
class NormalizedUser:
    """Normalized user model for consistent internal representation."""

    user_id: str
    email: str
    email_verified: bool
    name: Optional[str] = None
    provider: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
