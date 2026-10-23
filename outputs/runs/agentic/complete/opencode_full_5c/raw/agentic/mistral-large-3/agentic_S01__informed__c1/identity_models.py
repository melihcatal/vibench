from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: str


class RegisterUserResponse(BaseModel):
    success: bool
    user_id: Optional[str] = None
    email_verified: Optional[bool] = None
    error: Optional[str] = None


class LoginResponse(BaseModel):
    success: bool
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    error: Optional[str] = None


class RefreshSessionResponse(BaseModel):
    success: bool
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    error: Optional[str] = None


class PasswordResetResponse(BaseModel):
    success: bool
    reset_link: Optional[str] = None
    error: Optional[str] = None


class WelcomeTranslateRequest(BaseModel):
    text: str
    target_locale: str
    source_locale: Optional[str] = None


class WelcomeTranslateResponse(BaseModel):
    success: bool
    translated_text: Optional[str] = None
    error: Optional[str] = None


class ProfileModerationRequest(BaseModel):
    text: str


class ProfileModerationResponse(BaseModel):
    success: bool
    is_approved: Optional[bool] = None
    toxicity_score: Optional[float] = None
    error: Optional[str] = None


class OnboardingSummaryRequest(BaseModel):
    user_id: str
    steps_completed: List[str]
    context: Optional[Dict[str, Any]] = None


class OnboardingSummaryResponse(BaseModel):
    success: bool
    summary: Optional[str] = None
    error: Optional[str] = None


class ProfileNoteStoreRequest(BaseModel):
    user_id: str
    notes: str
    metadata: Dict[str, Any]


class ProfileNoteStoreResponse(BaseModel):
    success: bool
    document_id: Optional[str] = None
    error: Optional[str] = None


def normalize_firebase_error(error: Exception) -> str:
    """Normalizes Firebase-specific errors into user-friendly messages."""
    if isinstance(error, ValueError):
        return "Invalid input data."
    elif hasattr(error, "code"):
        if error.code == "email-already-exists":
            return "Email already in use."
        elif error.code == "invalid-email":
            return "Invalid email format."
        elif error.code == "user-not-found":
            return "User not found."
        elif error.code == "invalid-refresh-token":
            return "Invalid refresh token."
    return "An error occurred during authentication."
