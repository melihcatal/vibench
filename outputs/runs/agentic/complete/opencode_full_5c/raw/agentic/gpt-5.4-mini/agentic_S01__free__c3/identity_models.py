import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _lower_email(value: Any) -> str:
    return _clean_text(value).lower()


def _env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


@dataclass
class EmailPasswordIdentityRequest:
    email: str
    password: str
    locale: str = "en"

    @classmethod
    def from_mapping(cls, data: Dict[str, Any]) -> "EmailPasswordIdentityRequest":
        return cls(
            email=_lower_email(data.get("email")),
            password=_clean_text(data.get("password")),
            locale=_clean_text(data.get("locale"))
            or _env("IDENTITY_DEFAULT_LOCALE", "en"),
        )


@dataclass
class IdentityTokens:
    access_token: str
    refresh_token: str = ""
    expires_in: int = 0

    @classmethod
    def from_mapping(cls, data: Dict[str, Any]) -> "IdentityTokens":
        return cls(
            access_token=_clean_text(data.get("access_token") or data.get("idToken")),
            refresh_token=_clean_text(
                data.get("refresh_token") or data.get("refreshToken")
            ),
            expires_in=int(data.get("expires_in") or data.get("expiresIn") or 0),
        )


def normalize_email_password_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    request = EmailPasswordIdentityRequest.from_mapping(data)
    return {
        "email": request.email,
        "password": request.password,
        "locale": request.locale,
    }


def normalize_reset_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "email": _lower_email(data.get("email")),
        "locale": _clean_text(data.get("locale"))
        or _env("IDENTITY_DEFAULT_LOCALE", "en"),
    }


def identity_response(data: Dict[str, Any]) -> Dict[str, Any]:
    tokens = IdentityTokens.from_mapping(data)
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
        "expires_in": tokens.expires_in,
    }
