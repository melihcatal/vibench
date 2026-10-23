from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_locale(value: Optional[str]) -> str:
    if not value:
        return "en"
    return value.strip().replace("_", "-") or "en"


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


@dataclass
class AccountRequest:
    email: str
    password: str
    locale: str = "en"

    def normalized(self) -> Dict[str, Any]:
        return {
            "email": normalize_email(self.email),
            "password": self.password,
            "locale": normalize_locale(self.locale),
        }


@dataclass
class ResetRequest:
    email: str

    def normalized(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email)}


@dataclass
class NoteRecord:
    account_id: str
    note: str
    metadata: Dict[str, Any]
