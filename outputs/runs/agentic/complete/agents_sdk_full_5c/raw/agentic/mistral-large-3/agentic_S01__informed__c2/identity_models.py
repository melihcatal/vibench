# Local request, response, and normalization helpers for Email/Password Account Lifecycle

from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None


class RegisterUserResponse(BaseModel):
    user_id: str
    email: EmailStr
    created_at: str
    is_verified: bool


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class RefreshSessionResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetResponse(BaseModel):
    reset_initiated: bool
    reset_token: Optional[str] = None
    message: Optional[str] = None


def normalize_auth0_user_payload(payload: Dict[str, Any]) -> RegisterUserResponse:
    """Normalize Auth0 user creation response to local model."""
    return RegisterUserResponse(
        user_id=payload["user_id"],
        email=payload["email"],
        created_at=payload["created_at"],
        is_verified=payload.get("email_verified", False)
    )


def normalize_auth0_token_payload(payload: Dict[str, Any]) -> LoginResponse:
    """Normalize Auth0 token response to local model."""
    return LoginResponse(
        access_token=payload["access_token"],
        refresh_token=payload["refresh_token"],
        expires_in=payload["expires_in"],
        token_type=payload["token_type"]
    )