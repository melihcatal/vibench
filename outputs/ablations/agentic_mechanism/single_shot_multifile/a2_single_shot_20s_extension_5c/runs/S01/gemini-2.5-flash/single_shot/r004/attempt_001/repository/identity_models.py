from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserCredentials(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    idToken: str
    email: str
    refreshToken: str
    expiresIn: str
    localId: str
    registered: Optional[bool] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: str

class TranslateRequest(BaseModel):
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

class ModerationRequest(BaseModel):
    text_content: str
    text_type: Optional[str] = "plain"

class SummaryRequest(BaseModel):
    text: str
    max_tokens: Optional[int] = 150

class ProfileNote(BaseModel):
    user_id: str
    note_id: str # Unique ID for the note, could be timestamp based or UUID
    note_content: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
