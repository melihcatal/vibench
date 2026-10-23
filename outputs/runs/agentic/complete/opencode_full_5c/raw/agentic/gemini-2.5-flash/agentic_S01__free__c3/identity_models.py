from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    client_id: str
    user_pool_id: str
    username: Optional[str] = None


@dataclass
class UserRegistrationResponse:
    user_confirmed: bool
    user_sub: str


@dataclass
class UserLoginRequest:
    email: str
    password: str
    client_id: str
    user_pool_id: str


@dataclass
class UserLoginResponse:
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int


@dataclass
class RefreshSessionRequest:
    refresh_token: str
    client_id: str
    user_pool_id: str


@dataclass
class RefreshSessionResponse:
    access_token: str
    id_token: str
    expires_in: int


@dataclass
class PasswordResetRequest:
    email: str
    client_id: str
    user_pool_id: str


@dataclass
class PasswordResetResponse:
    message: str  # Or more detailed status


@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    project_id: str
    location: str = "global"


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class ProfileModerationRequest:
    text: str


@dataclass
class ProfileModerationResponse:
    sentiment: str
    sentiment_score: Dict[str, float]


@dataclass
class OnboardingSummaryRequest:
    onboarding_data: Dict[str, Any]


@dataclass
class OnboardingSummaryResponse:
    summary_text: str


@dataclass
class ProfileNote:
    user_id: str
    note_content: str
    timestamp: str
    metadata: Dict[str, Any]
