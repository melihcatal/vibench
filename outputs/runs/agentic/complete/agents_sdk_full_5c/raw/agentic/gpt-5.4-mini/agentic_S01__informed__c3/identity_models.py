from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    if not locale:
        return "en"
    return locale.replace("_", "-").strip().lower()


def normalize_text(text: Optional[str]) -> str:
    return (text or "").strip()


@dataclass(frozen=True)
class EmailPasswordRegistration:
    email: str
    password: str
    locale: str = "en"
    display_name: Optional[str] = None

    def payload(self) -> Dict[str, Any]:
        return {
            "email": normalize_email(self.email),
            "password": self.password,
            "locale": normalize_locale(self.locale),
            "display_name": normalize_text(self.display_name),
        }


@dataclass(frozen=True)
class EmailPasswordLoginRequest:
    email: str
    password: str

    def payload(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email), "password": self.password}


@dataclass(frozen=True)
class RefreshSessionRequest:
    refresh_token: str

    def payload(self) -> Dict[str, Any]:
        return {"refresh_token": self.refresh_token}


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    redirect_url: Optional[str] = None

    def payload(self) -> Dict[str, Any]:
        data = {"email": normalize_email(self.email)}
        if self.redirect_url:
            data["redirect_url"] = self.redirect_url
        return data


@dataclass(frozen=True)
class IdentityResult:
    success: bool
    provider: str
    data: Dict[str, Any]
    error: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)
