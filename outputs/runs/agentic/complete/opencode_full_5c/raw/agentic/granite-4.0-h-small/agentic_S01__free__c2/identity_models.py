# [HELPER] identity_models.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="User's password")


class AuthResponse(BaseModel):
    access_token: str = Field(
        ..., description="Bearer token for authenticated requests"
    )
    refresh_token: Optional[str] = Field(
        None, description="Token used to obtain new access tokens"
    )
    expires_in: int = Field(..., description="Lifetime of the access token in seconds")
    token_type: str = Field("Bearer", description="Token type")


class ResetPasswordRequest(BaseModel):
    email: EmailStr = Field(
        ..., description="User's email address to reset password for"
    )


class ResetPasswordResponse(BaseModel):
    ok: bool = True
    message: Optional[str] = None


class ProfileModerationRequest(BaseModel):
    profile_text: str = Field(..., description="Text submitted by user for profile")


class ProfileModerationResponse(BaseModel):
    moderated_text: str = Field(..., description="Text after moderation")
    action: str = Field(..., description="Action taken: approve, flag, reject")


class OnboardingSummaryRequest(BaseModel):
    user_id: str = Field(..., description="Identifier of the user")
    locale: str = Field("en", description="Locale for summary generation")


class OnboardingSummaryResponse(BaseModel):
    summary: str = Field(..., description="Summarized onboarding state for support")


class NoteStoreRequest(BaseModel):
    note_id: Optional[str] = None
    content: str = Field(..., description="Onboarding note or metadata")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class NoteStoreResponse(BaseModel):
    note_id: str = Field(..., description="Identifier of stored note")
    stored: bool = True
