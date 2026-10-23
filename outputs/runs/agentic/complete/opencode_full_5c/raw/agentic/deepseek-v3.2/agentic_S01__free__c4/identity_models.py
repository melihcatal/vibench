from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    display_name: Optional[str] = None


@dataclass
class UserRegistrationResponse:
    uid: str
    email: str
    display_name: str
    id_token: str
    refresh_token: str
    expires_in: str


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class LoginResponse:
    uid: str
    email: str
    display_name: str
    id_token: str
    refresh_token: str
    expires_in: str
    registered: bool


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class RefreshResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    token_type: str
    user_id: str
    project_id: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    email: str
    request_type: str
    success: bool
    message: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class ModerationRequest:
    text: str
    content_type: str = "profile"


@dataclass
class ModerationResponse:
    is_approved: bool
    flagged_categories: list
    confidence: float
    moderated_text: Optional[str] = None


@dataclass
class SummaryRequest:
    user_id: str
    onboarding_data: Dict[str, Any]


@dataclass
class SummaryResponse:
    user_id: str
    summary: str
    completion_percentage: float
    next_steps: list


@dataclass
class ProfileNote:
    user_id: str
    note_id: str
    content: str
    note_type: str
    created_at: str
    metadata: Dict[str, Any]
