from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RegisterUserRequest:
    email: str
    password: str


@dataclass
class RegisterUserResponse:
    uid: str
    email: str


@dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str


@dataclass
class EmailPasswordLoginResponse:
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str


@dataclass
class RefreshSessionRequest:
    refresh_token: str


@dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str
    expires_in: int


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    message: str


@dataclass
class TranslateRequest:
    text: str
    target_language: str


@dataclass
class TranslateResponse:
    translated_text: str


@dataclass
class ModerationRequest:
    text: str


@dataclass
class ModerationResponse:
    is_toxic: bool
    score: float


@dataclass
class OnboardingSummaryRequest:
    onboarding_data: str


@dataclass
class OnboardingSummaryResponse:
    summary: str


@dataclass
class ProfileNote:
    user_id: str
    note_id: str
    timestamp: str
    content: str
    metadata: dict


@dataclass
class ProfileNoteStoreRequest:
    user_id: str
    note_content: str
    metadata: dict


@dataclass
class ProfileNoteStoreResponse:
    note_id: str
