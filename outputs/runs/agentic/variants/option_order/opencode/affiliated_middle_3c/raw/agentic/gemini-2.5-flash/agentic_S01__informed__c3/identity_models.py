from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterUserResponse(BaseModel):
    user_id: str
    email: EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    id_token: Optional[str]
    expires_in: int


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetResponse(BaseModel):
    message: str


class TranslateRequest(BaseModel):
    text: str
    target_language: str


class TranslateResponse(BaseModel):
    translated_text: str


class ModerateProfileRequest(BaseModel):
    profile_text: str


class ModerateProfileResponse(BaseModel):
    is_safe: bool
    reason: Optional[str]


class SummarizeOnboardingRequest(BaseModel):
    onboarding_data: str


class SummarizeOnboardingResponse(BaseModel):
    summary: str


class StoreProfileNoteRequest(BaseModel):
    user_id: str
    note_content: str
    metadata: Optional[dict]


class StoreProfileNoteResponse(BaseModel):
    note_id: str
    status: str
