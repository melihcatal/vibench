from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

@datac,
class RegisterUserResponse:
    uid: str
    email: str
    display_name: Optional[str] = None

@dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str
    returnSecureToken: bool = True

@dataclass
class EmailPasswordLoginResponse:
    idToken: str
    refreshToken: str
    expiresIn: str
    isNewUser: bool
    email: str
    displayName: Optional[str] = None

@dataclass
class RefreshSessionRequest:
    grant_type: str = "refresh_token"
    refresh_token: str = None

@dataclass
class RefreshSessionResponse:
    access_token: str
    expires_in: str
    token_type: str
    refresh_token: str
    id_token: str
    user_id: str
    project_id: str

@dataclass
class PasswordResetRequest:
    email: str
    requestType: str = "PASSWORD_RESET"

@dataclass
class PasswordResetResponse:
    email: str

@dataclass
class TranslateRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class TranslateResponse:
    translated_text: str
    detected_language_code: Optional[str] = None

@dataclass
class ModerateProfileTextRequest:
    text_content: str
    user_id: str

@dataclass
class ModerateProfileTextResponse:
    is_safe: bool
    moderation_feedback: Optional[str] = None

@dataclass
class OnboardingSummaryRequest:
    user_id: str
    onboarding_data: Dict[str, Any]

@dataclass
class OnboardingSummaryResponse:
    summary_text: str

@dataclass
class ProfileNote:
    user_id: str
    note_content: str
    timestamp: str # ISO formatted string
    metadata: Dict[str, Any]

@dataclass
class StoreProfileNoteRequest:
    note: ProfileNote

@dataclass
class StoreProfileNoteResponse:
    note_id: str

