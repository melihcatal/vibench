from pydantic import BaseModel, Field
from typing import Optional

class UserRegistrationPayload(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None

class UserLoginPayload(BaseModel):
    email: str
    password: str

class TokenRefreshPayload(BaseModel):
    refresh_token: str

class PasswordResetPayload(BaseModel):
    email: str

class UserProfile(BaseModel):
    user_id: str
    email: str
    display_name: Optional[str] = None

class AuthTokens(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None

class ModerationRequest(BaseModel):
    text: str

class OnboardingSummaryRequest(BaseModel):
    user_id: str
    onboarding_steps_completed: list[str]
    profile_text: Optional[str] = None

class ProfileNote(BaseModel):
    user_id: str
    note_content: str
    category: str
