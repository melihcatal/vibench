from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional
import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(email: str) -> str:
    return email.strip().lower()


def ensure_email(email: str) -> str:
    normalized = normalize_email(email)
    if not _EMAIL_RE.match(normalized):
        raise ValueError("invalid email")
    return normalized


def normalize_locale(locale: Optional[str]) -> str:
    if not locale:
        return "en-US"
    return locale.replace("_", "-").strip() or "en-US"


def normalize_text(value: Optional[str]) -> str:
    return "" if value is None else str(value).strip()


@dataclass
class AccountRequest:
    email: str
    password: str
    locale: str = "en-US"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "AccountRequest":
        return AccountRequest(
            email=ensure_email(self.email),
            password=self.password,
            locale=normalize_locale(self.locale),
            metadata=dict(self.metadata),
        )


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"

    def as_dict(self) -> Dict[str, Any]:
        payload = {
            "access_token": self.access_token,
            "token_type": self.token_type,
        }
        if self.refresh_token is not None:
            payload["refresh_token"] = self.refresh_token
        if self.id_token is not None:
            payload["id_token"] = self.id_token
        if self.expires_in is not None:
            payload["expires_in"] = self.expires_in
        return payload


@dataclass
class LifecycleResponse:
    user_id: str
    email: str
    status: str
    message: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        data = {
            "user_id": self.user_id,
            "email": self.email,
            "status": self.status,
        }
        if self.message:
            data["message"] = self.message
        if self.raw:
            data["raw"] = self.raw
        return data


@dataclass
class OnboardingNote:
    account_id: str
    note: str
    locale: str = "en-US"
    support_metadata: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "account_id": self.account_id,
            "note": normalize_text(self.note),
            "locale": normalize_locale(self.locale),
            "support_metadata": dict(self.support_metadata),
        }


def extract_status(payload: Mapping[str, Any], default: str = "unknown") -> str:
    for key in ("status", "state", "result", "outcome"):
        value = payload.get(key)
        if value:
            return str(value)
    return default
