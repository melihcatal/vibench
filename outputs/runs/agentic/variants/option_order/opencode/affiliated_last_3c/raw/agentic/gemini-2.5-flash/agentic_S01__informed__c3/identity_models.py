import dataclasses
from typing import Optional


@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str


@dataclasses.dataclass
class RegisterUserResponse:
    user_id: str
    message: str


@dataclasses.dataclass
class LoginRequest:
    email: str
    password: str


@dataclasses.dataclass
class LoginResponse:
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int


@dataclasses.dataclass
class RefreshSessionRequest:
    refresh_token: str


@dataclasses.dataclass
class RefreshSessionResponse:
    access_token: str
    id_token: str
    expires_in: int


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
    source_language: Optional[str] = None


@dataclasses.dataclass
class TranslateResponse:
    translated_text: str


@dataclasses.dataclass
class ModerateTextRequest:
    text: str


@dataclasses.dataclass
class ModerateTextResponse:
    is_safe: bool
    reasons: list[str]


@dataclasses.dataclass
class SummarizeRequest:
    text: str


@dataclasses.dataclass
class SummarizeResponse:
    summary: str


@dataclasses.dataclass
class ProfileNote:
    user_id: str
    note_id: str
    timestamp: str
    content: str
    metadata: dict


@dataclasses.dataclass
class StoreProfileNoteRequest:
    user_id: str
    content: str
    metadata: dict


@dataclasses.dataclass
class StoreProfileNoteResponse:
    note_id: str
    message: str
