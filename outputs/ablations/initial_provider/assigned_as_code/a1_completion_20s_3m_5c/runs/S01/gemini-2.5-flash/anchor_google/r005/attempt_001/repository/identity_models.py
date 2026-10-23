from pydantic import BaseModel
from typing import Optional, Dict, Any

class RegisterUserPayload(BaseModel):
    email: str
    password: str

class LoginPayload(BaseModel):
    email: str
    password: str

class RefreshSessionPayload(BaseModel):
    refresh_token: str

class PasswordResetPayload(BaseModel):
    email: str

class TranslatePayload(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None

class ModerateProfilePayload(BaseModel):
    profile_text: str

class OnboardingSummaryPayload(BaseModel):
    user_id: str
    onboarding_data: Dict[str, Any]

class ProfileNoteStorePayload(BaseModel):
    user_id: str
    note_content: str
    metadata: Optional[Dict[str, Any]] = None
