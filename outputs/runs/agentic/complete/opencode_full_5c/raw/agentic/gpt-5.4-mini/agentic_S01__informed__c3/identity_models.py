from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    if not locale:
        return "en"
    return locale.strip().replace("_", "-").lower()


def compact_text(value: Optional[str]) -> str:
    return " ".join((value or "").split()).strip()


@dataclass
class EmailPasswordRegistration:
    email: str
    password: str
    locale: str = "en"
    display_name: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        return {
            "email": normalize_email(self.email),
            "password": self.password,
            "locale": normalize_locale(self.locale),
            "display_name": compact_text(self.display_name),
        }


@dataclass
class EmailPasswordLogin:
    email: str
    password: str

    def normalized(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email), "password": self.password}


@dataclass
class PasswordResetRequest:
    email: str

    def normalized(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email)}


def token_bundle(
    access_token: Optional[str],
    refresh_token: Optional[str],
    id_token: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "id_token": id_token,
    }


def response_payload(
    provider: str, action: str, data: Dict[str, Any]
) -> Dict[str, Any]:
    payload = {"provider": provider, "action": action}
    payload.update(data)
    return payload
