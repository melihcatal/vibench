
"""
Define local request, response, and normalization helpers for Email/Password Account Lifecycle.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str

@dataclass
class AuthTokens:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"

@dataclass
class LoginResponse:
    tokens: AuthTokens
    user_id: str

@dataclass
class RegisterUserRequest:
    email: str
    password: str
    confirm_password: str
    display_name: Optional[str] = None

@dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    display_name: Optional[str] = None

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    message: str = "Password reset email sent if account exists."

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    tokens: AuthTokens
    user_id: str

def normalize_email(email: str) -> str:
    """Normalizes an email address to a consistent format."""
    return email.strip().lower()

def parse_auth_response(response_data: Dict[str, Any]) -> AuthTokens:
    """Parses raw authentication response data into an AuthTokens object."""
    return AuthTokens(
        access_token=response_data.get("accessToken") or response_data.get("idToken"),
        refresh_token=response_data.get("refreshToken"),
        expires_in=response_data.get("expiresIn"),
        token_type=response_data.get("tokenType", "Bearer")
    )

