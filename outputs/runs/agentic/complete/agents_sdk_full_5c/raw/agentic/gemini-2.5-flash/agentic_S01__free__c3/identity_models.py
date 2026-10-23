from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RegisterRequest:
    email: str
    password: str

@dataclass
class RegisterResponse:
    uid: str
    email: str

@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass
class LoginResponse:
    id_token: str
    refresh_token: str
    expires_in: int
    uid: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str
    expires_in: int
    uid: Optional[str] = None # UID might be included but not always

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    email: str

@dataclass
class WelcomeMessageTranslateRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class WelcomeMessageTranslateResponse:
    translated_text: str
    detected_source_language: str

@dataclass
class ProfileModerationRequest:
    text: str

@dataclass
class ProfileModerationScore:
    attribute: str
    score: float

@dataclass
class ProfileModerationResponse:
    is_flagged: bool
    scores: list[ProfileModerationScore] = field(default_factory=list)

@dataclass
class OnboardingSummaryRequest:
    onboarding_data: dict

@dataclass
class OnboardingSummaryResponse:
    summary: str

@dataclass
class ProfileNote:
    user_id: str
    note_id: str
    timestamp: float
    content: str
    metadata: dict = field(default_factory=dict)

@dataclass
class StoreProfileNoteRequest:
    user_id: str
    content: str
    metadata: Optional[dict] = None

@dataclass
class StoreProfileNoteResponse:
    note_id: str
    timestamp: float
