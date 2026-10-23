"""
Local request, response, and normalization helpers for Email/Password Account Lifecycle.

Provides Pydantic models for normalizing payloads exchanged with Firebase Authentication
and downstream services across the account lifecycle.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    display_name: Optional[str] = None
    locale: Optional[str] = Field(default="en-US", pattern=r"^[a-z]{2}(-[A-Z]{2})?$")
    metadata: Optional[Dict[str, str]] = None


class RegisterUserResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None
    created_at: datetime
    locale: Optional[str] = None
    raw_firebase_payload: Optional[Dict[str, Any]] = None

    @classmethod
    def from_firebase_user_record(cls, user_record: Any) -> "RegisterUserResponse":
        return cls(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            created_at=datetime.fromtimestamp(
                user_record.user_metadata.creation_timestamp / 1000.0, tz=timezone.utc
            ),
            locale=user_record.custom_data.get("locale")
            if getattr(user_record, "custom_data", None)
            else None,
            raw_firebase_payload=None,
        )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    return_secure_token: bool = Field(default=True)


class LoginResponse(BaseModel):
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str
    email: Optional[EmailStr] = None
    registered: bool = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    grant_type: str = Field(default="refresh_token")


class RefreshTokenResponse(BaseModel):
    id_token: str
    expires_in: int
    token_type: str = Field(default="Bearer")
    refresh_token: Optional[str] = None


class PasswordResetRequest(BaseModel):
    email: EmailStr
    continue_url: Optional[str] = None
    locale: Optional[str] = Field(default="en", pattern=r"^[a-z]{2}$")


class PasswordResetResponse(BaseModel):
    email: EmailStr
    reset_link: Optional[str] = None
    oob_code: Optional[str] = None
    status: str = Field(default="initiated")


class UserProfilePayload(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    locale: Optional[str] = "en-US"


class OnboardingState(BaseModel):
    uid: str
    email: str
    locale: Optional[str] = "en-US"
    steps_completed: List[str] = Field(default_factory=list)
    profile: Optional[UserProfilePayload] = None
    moderation_status: Optional[str] = None
    notes: Optional[str] = None


def normalize_login_response(api_payload: Dict[str, Any]) -> LoginResponse:
    return LoginResponse(
        id_token=api_payload.get("idToken", ""),
        refresh_token=api_payload.get("refreshToken", ""),
        expires_in=int(api_payload.get("expiresIn", "3600")),
        local_id=api_payload.get("localId", ""),
        email=api_payload.get("email"),
        registered=api_payload.get("registered", True),
    )


def normalize_refresh_response(api_payload: Dict[str, Any]) -> RefreshTokenResponse:
    return RefreshTokenResponse(
        id_token=api_payload.get("id_token", ""),
        expires_in=int(api_payload.get("expires_in", "3600")),
        token_type=api_payload.get("token_type", "Bearer"),
        refresh_token=api_payload.get("refresh_token"),
    )


def normalize_password_reset_response(api_payload: Dict[str, Any]) -> PasswordResetResponse:
    return PasswordResetResponse(
        email=api_payload.get("email", ""),
        oob_code=api_payload.get("oobCode"),
        status="initiated",
    )
