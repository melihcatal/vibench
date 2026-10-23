from pydantic import BaseModel
from typing import Optional, Dict, Any

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    id_token: str
    refresh_token: str
    expires_in: str

class RefreshSessionRequest(BaseModel):
    refresh_token: str

class RefreshSessionResponse(BaseModel):
    id_token: str
    refresh_token: str
    expires_in: str

class PasswordResetRequest(BaseModel):
    email: str

class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None

class TranslateResponse(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = None

class ProfileModerationRequest(BaseModel):
    profile_text: str

class ProfileModerationResponse(BaseModel):
    is_safe: bool
    reasons: Optional[Dict[str, float]] = None

class OnboardingSummaryRequest(BaseModel):
    onboarding_data: Dict[str, Any]

class OnboardingSummaryResponse(BaseModel):
    summary_text: str

class NoteStoreRequest(BaseModel):
    user_id: str
    note_type: str
    content: Dict[str, Any]

class NoteStoreResponse(BaseModel):
    document_id: str
    status: str
