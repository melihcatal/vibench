from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip().replace("_", "-")
    return value or "en"


def normalize_text(text: Optional[str]) -> str:
    return (text or "").strip()


@dataclass
class AccountRequest:
    email: str
    password: str
    locale: str = "en"

    def to_payload(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email), "password": self.password, "locale": normalize_locale(self.locale)}


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SupportNote:
    user_id: str
    note: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
