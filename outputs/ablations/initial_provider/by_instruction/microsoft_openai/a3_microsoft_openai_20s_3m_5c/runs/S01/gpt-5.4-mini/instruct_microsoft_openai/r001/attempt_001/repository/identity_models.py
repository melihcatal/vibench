from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip()
    return value if value else "en"


@dataclass
class EmailPasswordRequest:
    email: str
    password: str
    locale: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str]
    expires_in: Optional[int]
    token_type: str


def as_dict(data: Any) -> Dict[str, Any]:
    if hasattr(data, "__dict__"):
        return dict(data.__dict__)
    return dict(data)
