import dataclasses
from typing import Optional


@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str


@dataclasses.dataclass
class RegisterUserResponse:
    uid: str
    email: str
    id_token: str
    refresh_token: str


@dataclasses.dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str


@dataclasses.dataclass
class EmailPasswordLoginResponse:
    uid: str
    email: str
    id_token: str
    refresh_token: str


@dataclasses.dataclass
class RefreshSessionRequest:
    refresh_token: str


@dataclasses.dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str


@dataclasses.dataclass
class PasswordResetRequest:
    email: str


@dataclasses.dataclass
class PasswordResetResponse:
    message: str


@dataclasses.dataclass
class TranslateRequest:
    text: str
    target_language: str


@dataclasses.dataclass
class TranslateResponse:
    translated_text: str


@dataclasses.dataclass
class ModerateProfileRequest:
    profile_text: str


@dataclasses.dataclass
class ModerateProfileResponse:
    is_safe: bool
    score: Optional[float]


@dataclasses.dataclass
class OnboardingSummaryRequest:
    onboarding_data: str


@dataclasses.dataclass
class OnboardingSummaryResponse:
    summary: str


@dataclasses.dataclass
class ProfileNoteStoreRequest:
    user_id: str
    note_content: str
    metadata: dict


@dataclasses.dataclass
class ProfileNoteStoreResponse:
    document_id: str
