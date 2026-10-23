from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip().replace("_", "-")
    return value or "en"


def normalize_profile_text(text: Optional[str]) -> str:
    return (text or "").strip()


@dataclass
class EmailPasswordRequest:
    email: str
    password: str


@dataclass
class EmailPasswordResponse:
    user_id: str
    email: str
    tokens: Dict[str, Any]
