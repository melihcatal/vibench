from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
import re


_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def normalize_email(email: str) -> str:
    if email is None:
        raise ValueError("email is required")
    value = email.strip().lower()
    if not value:
        raise ValueError("email is required")
    if not _EMAIL_RE.match(value):
        raise ValueError("invalid email")
    return value


def normalize_password(password: str) -> str:
    if password is None:
        raise ValueError("password is required")
    value = password.strip()
    if not value:
        raise ValueError("password is required")
    return value


def normalize_display_name(display_name: Optional[str]) -> Optional[str]:
    if display_name is None:
        return None
    value = display_name.strip()
    return value or None


@dataclass(frozen=True)
class AccountCreateRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def normalized(self) -> "AccountCreateRequest":
        return AccountCreateRequest(
            email=normalize_email(self.email),
            password=normalize_password(self.password),
            display_name=normalize_display_name(self.display_name),
        )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountCreateRequest":
        return cls(
            email=str(data.get("email", "")),
            password=str(data.get("password", "")),
            display_name=data.get("display_name"),
        ).normalized()


@dataclass(frozen=True)
class AccountLoginRequest:
    email: str
    password: str

    def normalized(self) -> "AccountLoginRequest":
        return AccountLoginRequest(
            email=normalize_email(self.email),
            password=normalize_password(self.password),
        )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountLoginRequest":
        return cls(
            email=str(data.get("email", "")),
            password=str(data.get("password", "")),
        ).normalized()


@dataclass(frozen=True)
class AccountUpdateRequest:
    email: Optional[str] = None
    password: Optional[str] = None
    display_name: Optional[str] = None

    def normalized(self) -> "AccountUpdateRequest":
        return AccountUpdateRequest(
            email=normalize_email(self.email) if self.email is not None else None,
            password=normalize_password(self.password) if self.password is not None else None,
            display_name=normalize_display_name(self.display_name),
        )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountUpdateRequest":
        return cls(
            email=data.get("email"),
            password=data.get("password"),
            display_name=data.get("display_name"),
        ).normalized()


@dataclass(frozen=True)
class AccountResponse:
    id: str
    email: str
    display_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountResponse":
        return cls(
            id=str(data.get("id", "")),
            email=normalize_email(str(data.get("email", ""))),
            display_name=normalize_display_name(data.get("display_name")),
            is_active=bool(data.get("is_active", True)),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str

    def normalized(self) -> "PasswordResetRequest":
        return PasswordResetRequest(email=normalize_email(self.email))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PasswordResetRequest":
        return cls(email=str(data.get("email", ""))).normalized()


@dataclass(frozen=True)
class PasswordResetConfirmRequest:
    token: str
    new_password: str

    def normalized(self) -> "PasswordResetConfirmRequest":
        return PasswordResetConfirmRequest(
            token=self.token.strip(),
            new_password=normalize_password(self.new_password),
        )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PasswordResetConfirmRequest":
        return cls(
            token=str(data.get("token", "")),
            new_password=str(data.get("new_password", "")),
        ).normalized()


@dataclass(frozen=True)
class LifecycleStatusResponse:
    success: bool
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, message: str = "", **details: Any) -> "LifecycleStatusResponse":
        return cls(success=True, message=message, details=dict(details))

    @classmethod
    def error(cls, message: str, **details: Any) -> "LifecycleStatusResponse":
        return cls(success=False, message=message, details=dict(details))
