import re
from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip().replace("_", "-")
    return value or "en"


def normalize_profile_text(text: Optional[str]) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


@dataclass
class AccountRequest:
    email: str
    password: str
    locale: str = "en"

    def payload(self) -> Dict[str, Any]:
        return {
            "email": normalize_email(self.email),
            "password": self.password,
            "locale": normalize_locale(self.locale),
        }


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class ResetRequest:
    email: str

    def payload(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email)}
