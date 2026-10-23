from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _normalize_password(password: str) -> str:
    return password.strip()


def _normalize_optional_str(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _mapping_get(data: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data:
            return data[key]
    return None


@dataclass(frozen=True)
class AccountCreateRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountCreateRequest":
        return cls(
            email=_normalize_email(str(_mapping_get(data, "email", "email_address"))),
            password=_normalize_password(str(_mapping_get(data, "password", "secret"))),
            display_name=_normalize_optional_str(
                None if _mapping_get(data, "display_name", "name") is None else str(_mapping_get(data, "display_name", "name"))
            ),
        )

    def normalized(self) -> "AccountCreateRequest":
        return AccountCreateRequest(
            email=_normalize_email(self.email),
            password=_normalize_password(self.password),
            display_name=_normalize_optional_str(self.display_name),
        )


@dataclass(frozen=True)
class AccountLoginRequest:
    email: str
    password: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountLoginRequest":
        return cls(
            email=_normalize_email(str(_mapping_get(data, "email", "email_address"))),
            password=_normalize_password(str(_mapping_get(data, "password", "secret"))),
        )

    def normalized(self) -> "AccountLoginRequest":
        return AccountLoginRequest(
            email=_normalize_email(self.email),
            password=_normalize_password(self.password),
        )


@dataclass(frozen=True)
class AccountUpdatePasswordRequest:
    current_password: str
    new_password: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountUpdatePasswordRequest":
        return cls(
            current_password=_normalize_password(str(_mapping_get(data, "current_password", "old_password"))),
            new_password=_normalize_password(str(_mapping_get(data, "new_password", "password"))),
        )

    def normalized(self) -> "AccountUpdatePasswordRequest":
        return AccountUpdatePasswordRequest(
            current_password=_normalize_password(self.current_password),
            new_password=_normalize_password(self.new_password),
        )


@dataclass(frozen=True)
class AccountLifecycleResponse:
    success: bool
    account_id: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccountLifecycleResponse":
        return cls(
            success=bool(_mapping_get(data, "success")),
            account_id=_normalize_optional_str(None if _mapping_get(data, "account_id", "id") is None else str(_mapping_get(data, "account_id", "id"))),
            email=_normalize_optional_str(None if _mapping_get(data, "email", "email_address") is None else str(_mapping_get(data, "email", "email_address"))),
            display_name=_normalize_optional_str(None if _mapping_get(data, "display_name", "name") is None else str(_mapping_get(data, "display_name", "name"))),
            status=_normalize_optional_str(None if _mapping_get(data, "status") is None else str(_mapping_get(data, "status"))),
            message=_normalize_optional_str(None if _mapping_get(data, "message", "detail") is None else str(_mapping_get(data, "message", "detail"))),
            metadata=dict(_mapping_get(data, "metadata") or {}),
        )

    def normalized(self) -> "AccountLifecycleResponse":
        return AccountLifecycleResponse(
            success=bool(self.success),
            account_id=_normalize_optional_str(self.account_id),
            email=_normalize_optional_str(self.email),
            display_name=_normalize_optional_str(self.display_name),
            status=_normalize_optional_str(self.status),
            message=_normalize_optional_str(self.message),
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class AccountLifecycleRecord:
    request: AccountCreateRequest | AccountLoginRequest | AccountUpdatePasswordRequest
    response: Optional[AccountLifecycleResponse] = None
    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def touch(self) -> "AccountLifecycleRecord":
        return AccountLifecycleRecord(
            request=self.request,
            response=self.response,
            created_at=self.created_at,
            updated_at=_utc_now(),
        )
