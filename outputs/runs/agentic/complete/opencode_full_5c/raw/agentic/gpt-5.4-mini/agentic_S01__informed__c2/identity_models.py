from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    if not locale:
        return "en"
    return locale.replace("_", "-").strip().lower()


def pick_dict(data: Any) -> Dict[str, Any]:
    return data if isinstance(data, dict) else {}


@dataclass
class AccountRequest:
    email: str
    password: Optional[str] = None
    locale: Optional[str] = None
    name: Optional[str] = None


@dataclass
class AccountResponse:
    ok: bool
    data: Dict[str, Any]
    error: Optional[str] = None
