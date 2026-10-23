from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip().replace("_", "-")
    return value or "en"


@dataclass
class RegistrationRequest:
    email: str
    password: str
    locale: str = "en"
    full_name: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        payload = {
            "email": normalize_email(self.email),
            "password": self.password,
            "locale": normalize_locale(self.locale),
        }
        if self.full_name:
            payload["full_name"] = self.full_name.strip()
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str

    def as_dict(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email), "password": self.password}


@dataclass
class RefreshRequest:
    refresh_token: str

    def as_dict(self) -> Dict[str, Any]:
        return {"refresh_token": self.refresh_token.strip()}


@dataclass
class PasswordResetRequest:
    email: str

    def as_dict(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email)}
