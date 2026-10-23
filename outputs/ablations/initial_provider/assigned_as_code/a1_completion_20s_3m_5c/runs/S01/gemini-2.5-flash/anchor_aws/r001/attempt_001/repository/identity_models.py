from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class UserRegistration(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int
    token_type: str

class RefreshSessionRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: str

class ProfileText(BaseModel):
    text: str
    language_code: Optional[str] = None

class OnboardingSummaryRequest(BaseModel):
    user_id: str
    onboarding_data: Dict[str, Any]

class ProfileNote(BaseModel):
    user_id: str
    note_content: str
    timestamp: Optional[str] = None
