from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip().replace("_", "-")
    return value or "en"


@dataclass
class AccountCredentials:
    email: str
    password: str
    locale: str = "en"


@dataclass
class TokenPair:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class ResetRequest:
    email: str


@dataclass
class ManagedNote:
    subject_id: str
    note: str
    metadata: Dict[str, Any]
