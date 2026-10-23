import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


def clean_email(value: str) -> str:
    return value.strip().lower()


def clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = value.strip()
    return text or None


def env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip()


@dataclass
class AccountRequest:
    email: str
    password: str

    def normalized(self) -> "AccountRequest":
        return AccountRequest(email=clean_email(self.email), password=self.password)


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class ResetRequest:
    email: str

    def normalized(self) -> "ResetRequest":
        return ResetRequest(email=clean_email(self.email))


def coerce_token_response(payload: Dict[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=str(payload.get("access_token", "")),
        refresh_token=payload.get("refresh_token"),
        expires_in=payload.get("expires_in"),
        raw=payload,
    )
