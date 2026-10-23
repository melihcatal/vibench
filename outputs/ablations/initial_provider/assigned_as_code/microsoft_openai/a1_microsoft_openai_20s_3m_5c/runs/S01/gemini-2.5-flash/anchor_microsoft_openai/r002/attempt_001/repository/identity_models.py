from pydantic import BaseModel, Field
from typing import Optional

class UserCredentials(BaseModel):
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str

class UserProfile(BaseModel):
    user_id: str
    display_name: str
    email: str
    locale: Optional[str] = None
    profile_text: Optional[str] = None

class PasswordResetRequest(BaseModel):
    email: str

class TranslatedContent(BaseModel):
    text: str
    language_code: str

class ModerationResult(BaseModel):
    is_safe: bool
    reasons: list[str]

class OnboardingSummary(BaseModel):
    user_id: str
    summary_text: str

class ProfileNote(BaseModel):
    user_id: str
    note_id: str
    timestamp: str
    content: str
    metadata: dict
