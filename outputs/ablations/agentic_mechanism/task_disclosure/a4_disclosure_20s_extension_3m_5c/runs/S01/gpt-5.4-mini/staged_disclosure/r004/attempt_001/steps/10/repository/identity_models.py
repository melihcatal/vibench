from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from typing import Any, Mapping, Optional


_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_email(email: str) -> str:
    value = email.strip().lower()
    if not value or not _EMAIL_RE.match(value):
        raise ValueError("invalid email address")
    return value


def _normalize_password(password: str) -> str:
    if password is None:
        raise ValueError("password is required")
    value = password.strip()
    if len(value) < 8:
        raise ValueError("password must be at least 8 characters")
    return value


def _normalize_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


@dataclass(frozen=True)
class AccountCreateRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "email", _normalize_email(self.email))
        object.__setattr__(self, "password", _normalize_password(self.password))
        object.__setattr__(self, "display_name", _normalize_string(self.display_name))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountCreateRequest":
        return cls(
            email=str(data.get("email", "")),
            password=str(data.get("password", "")),
            display_name=_normalize_string(data.get("display_name")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = {"email": self.email, "password": self.password}
        if self.display_name is not None:
            payload["display_name"] = self.display_name
        return payload


@dataclass(frozen=True)
class AccountUpdateRequest:
    email: Optional[str] = None
    password: Optional[str] = None
    display_name: Optional[str] = None

    def __post_init__(self) -> None:
        if self.email is not None:
            object.__setattr__(self, "email", _normalize_email(self.email))
        if self.password is not None:
            object.__setattr__(self, "password", _normalize_password(self.password))
        object.__setattr__(self, "display_name", _normalize_string(self.display_name))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountUpdateRequest":
        return cls(
            email=data.get("email"),
            password=data.get("password"),
            display_name=data.get("display_name"),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.email is not None:
            payload["email"] = self.email
        if self.password is not None:
            payload["password"] = self.password
        if self.display_name is not None:
            payload["display_name"] = self.display_name
        return payload


@dataclass(frozen=True)
class AccountLoginRequest:
    email: str
    password: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "email", _normalize_email(self.email))
        object.__setattr__(self, "password", _normalize_password(self.password))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountLoginRequest":
        return cls(email=str(data.get("email", "")), password=str(data.get("password", "")))

    def to_dict(self) -> dict[str, Any]:
        return {"email": self.email, "password": self.password}


@dataclass(frozen=True)
class AccountResponse:
    account_id: str
    email: str
    display_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=_utcnow)
    updated_at: datetime = field(default_factory=_utcnow)

    def __post_init__(self) -> None:
        object.__setattr__(self, "account_id", str(self.account_id).strip())
        object.__setattr__(self, "email", _normalize_email(self.email))
        object.__setattr__(self, "display_name", _normalize_string(self.display_name))
        object.__setattr__(self, "is_active", bool(self.is_active))
        if self.created_at.tzinfo is None:
            object.__setattr__(self, "created_at", self.created_at.replace(tzinfo=timezone.utc))
        if self.updated_at.tzinfo is None:
            object.__setattr__(self, "updated_at", self.updated_at.replace(tzinfo=timezone.utc))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountResponse":
        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        return cls(
            account_id=str(data.get("account_id", data.get("id", ""))),
            email=str(data.get("email", "")),
            display_name=data.get("display_name"),
            is_active=bool(data.get("is_active", True)),
            created_at=_parse_datetime(created_at) if created_at else _utcnow(),
            updated_at=_parse_datetime(updated_at) if updated_at else _utcnow(),
        )

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "account_id": self.account_id,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if self.display_name is not None:
            payload["display_name"] = self.display_name
        return payload


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "email", _normalize_email(self.email))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PasswordResetRequest":
        return cls(email=str(data.get("email", "")))

    def to_dict(self) -> dict[str, Any]:
        return {"email": self.email}


@dataclass(frozen=True)
class PasswordResetResponse:
    email: str
    reset_token: str
    expires_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "email", _normalize_email(self.email))
        object.__setattr__(self, "reset_token", str(self.reset_token).strip())
        if self.expires_at.tzinfo is None:
            object.__setattr__(self, "expires_at", self.expires_at.replace(tzinfo=timezone.utc))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PasswordResetResponse":
        return cls(
            email=str(data.get("email", "")),
            reset_token=str(data.get("reset_token", "")),
            expires_at=_parse_datetime(data.get("expires_at")) if data.get("expires_at") else _utcnow(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"email": self.email, "reset_token": self.reset_token, "expires_at": self.expires_at.isoformat()}


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)
