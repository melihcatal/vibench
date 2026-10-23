from pydantic import BaseModel, Field
from typing import Optional


class UserRegisterPayload(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserLoginPayload(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class RefreshSessionPayload(BaseModel):
    refresh_token: str = Field(..., description="The refresh token for the session")


class PasswordResetPayload(BaseModel):
    email: str = Field(..., description="User's email address for password reset")


class UserProfileText(BaseModel):
    text: str = Field(..., description="User provided profile text")


class OnboardingTranslationPayload(BaseModel):
    text: str = Field(..., description="Text to translate")
    target_language: str = Field(..., description="Target language code (e.g., 'es', 'fr')")


class OnboardingSummaryPayload(BaseModel):
    onboarding_data: dict = Field(..., description="Onboarding data to summarize")


class ProfileNotePayload(BaseModel):
    user_id: str = Field(..., description="User ID associated with the note")
    note_content: str = Field(..., description="Content of the note")
    metadata: Optional[dict] = Field(None, description="Optional metadata for the note")


class AuthTokens(BaseModel):
    id_token: str = Field(..., description="Firebase ID token")
    refresh_token: str = Field(..., description="Firebase refresh token")
    expires_in: int = Field(..., description="Time until ID token expires, in seconds")
    local_id: str = Field(..., description="User's Firebase Local ID")
