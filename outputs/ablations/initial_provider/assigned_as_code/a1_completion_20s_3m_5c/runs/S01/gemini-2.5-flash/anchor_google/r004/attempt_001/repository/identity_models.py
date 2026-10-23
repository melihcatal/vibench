from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterUserPayload(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LoginUserPayload(BaseModel):
    email: EmailStr
    password: str


class RefreshSessionPayload(BaseModel):
    refresh_token: str


class PasswordResetPayload(BaseModel):
    email: EmailStr


class UserInfo(BaseModel):
    uid: str
    email: Optional[EmailStr] = None


class AuthTokens(BaseModel):
    id_token: str
    refresh_token: str
    expires_in: int


class WelcomeTranslatePayload(BaseModel):
    user_id: str
    locale: str
    welcome_message: str


class ProfileModerationPayload(BaseModel):
    user_id: str
    profile_text: str


class OnboardingSummaryPayload(BaseModel):
    user_id: str
    onboarding_data: dict


class ProfileNoteStorePayload(BaseModel):
    user_id: str
    note_content: str
    metadata: dict
