from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en-US").strip()
    return value or "en-US"


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    locale: str = "en-US"


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class TranslationRequest:
    text: str
    locale: str


@dataclass
class ModerationRequest:
    text: str


@dataclass
class SummaryRequest:
    account_id: str
    state: Dict[str, Any]


@dataclass
class NoteStoreRequest:
    account_id: str
    note: str
    metadata: Dict[str, Any]
