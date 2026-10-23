from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional
import re


_WHITESPACE_RE = re.compile(r"\s+")


def normalize_email(email: str) -> str:
    if email is None:
        raise ValueError("email is required")
    value = email.strip().lower()
    if not value:
        raise ValueError("email is required")
    if "@" not in value or value.startswith("@") or value.endswith("@"):
        raise ValueError("email is invalid")
    local, domain = value.rsplit("@", 1)
    if not local or not domain or "." not in domain:
        raise ValueError("email is invalid")
    return value


def normalize_username(username: Optional[str]) -> Optional[str]:
    if username is None:
        return None
    value = _WHITESPACE_RE.sub(" ", username.strip())
    return value or None


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    if phone is None:
        return None
    value = re.sub(r"[^0-9+]", "", phone.strip())
    return value or None


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if locale is None:
        return None
    value = locale.strip().replace("_", "-").lower()
    return value or None


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get(mapping: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


@dataclass(frozen=True)
class EmailPasswordCredentials:
    email: str
    password: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "EmailPasswordCredentials":
        return cls(email=normalize_email(str(_get(data, "email"))), password=str(_get(data, "password") or ""))

    def normalized(self) -> "EmailPasswordCredentials":
        return EmailPasswordCredentials(email=normalize_email(self.email), password=self.password)


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    locale: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RegisterUserRequest":
        return cls(
            email=normalize_email(str(_get(data, "email"))),
            password=str(_get(data, "password") or ""),
            display_name=normalize_username(_get(data, "display_name", "displayName")),
            locale=normalize_locale(_get(data, "locale")),
            metadata=dict(_get(data, "metadata") or {}),
        )

    def normalized(self) -> "RegisterUserRequest":
        return RegisterUserRequest(
            email=normalize_email(self.email),
            password=self.password,
            display_name=normalize_username(self.display_name),
            locale=normalize_locale(self.locale),
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "LoginRequest":
        return cls(email=normalize_email(str(_get(data, "email"))), password=str(_get(data, "password") or ""))


@dataclass(frozen=True)
class RefreshSessionRequest:
    refresh_token: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RefreshSessionRequest":
        token = str(_get(data, "refresh_token", "refreshToken") or "").strip()
        if not token:
            raise ValueError("refresh_token is required")
        return cls(refresh_token=token)


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    redirect_url: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PasswordResetRequest":
        return cls(
            email=normalize_email(str(_get(data, "email"))),
            redirect_url=str(_get(data, "redirect_url", "redirectUrl") or "").strip() or None,
        )


@dataclass(frozen=True)
class ProfileModerationRequest:
    profile_text: str
    locale: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ProfileModerationRequest":
        text = str(_get(data, "profile_text", "profileText", "text") or "").strip()
        if not text:
            raise ValueError("profile_text is required")
        return cls(profile_text=text, locale=normalize_locale(_get(data, "locale")))


@dataclass(frozen=True)
class OnboardingSummaryRequest:
    user_id: str
    locale: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "OnboardingSummaryRequest":
        user_id = str(_get(data, "user_id", "userId") or "").strip()
        if not user_id:
            raise ValueError("user_id is required")
        return cls(user_id=user_id, locale=normalize_locale(_get(data, "locale")))


@dataclass(frozen=True)
class BaseResponse:
    ok: bool = True
    message: Optional[str] = None
    request_id: Optional[str] = None
    created_at: str = field(default_factory=utc_now_iso)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "message": self.message,
            "request_id": self.request_id,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class TokenPairResponse(BaseResponse):
    user_id: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None

    def as_dict(self) -> dict[str, Any]:
        data = super().as_dict()
        data.update(
            {
                "user_id": self.user_id,
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "token_type": self.token_type,
                "expires_in": self.expires_in,
            }
        )
        return data


@dataclass(frozen=True)
class UserProfileResponse(BaseResponse):
    user_id: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    locale: Optional[str] = None
    email_verified: bool = False
    active: bool = True

    def as_dict(self) -> dict[str, Any]:
        data = super().as_dict()
        data.update(
            {
                "user_id": self.user_id,
                "email": self.email,
                "display_name": self.display_name,
                "locale": self.locale,
                "email_verified": self.email_verified,
                "active": self.active,
            }
        )
        return data


def normalize_user_profile(data: Mapping[str, Any]) -> dict[str, Any]:
    email = _get(data, "email")
    display_name = _get(data, "display_name", "displayName")
    locale = _get(data, "locale")
    normalized = {
        "user_id": str(_get(data, "user_id", "userId") or "").strip() or None,
        "email": normalize_email(str(email)) if email is not None else None,
        "display_name": normalize_username(display_name),
        "locale": normalize_locale(locale),
        "email_verified": bool(_get(data, "email_verified", "emailVerified") or False),
        "active": bool(_get(data, "active") if _get(data, "active") is not None else True),
    }
    return normalized


def normalize_token_response(data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "user_id": str(_get(data, "user_id", "userId") or "").strip() or None,
        "access_token": str(_get(data, "access_token", "accessToken") or "").strip() or None,
        "refresh_token": str(_get(data, "refresh_token", "refreshToken") or "").strip() or None,
        "token_type": str(_get(data, "token_type", "tokenType") or "Bearer").strip() or "Bearer",
        "expires_in": int(_get(data, "expires_in", "expiresIn")) if _get(data, "expires_in", "expiresIn") is not None else None,
    }
