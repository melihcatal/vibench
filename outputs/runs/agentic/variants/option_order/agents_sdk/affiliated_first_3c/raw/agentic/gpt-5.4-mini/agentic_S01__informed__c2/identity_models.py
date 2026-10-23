from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


@dataclass(slots=True)
class EmailPasswordIdentityRequest:
    email: str
    password: Optional[str] = None
    locale: Optional[str] = None
    display_name: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_email(self) -> str:
        return self.email.strip().lower()


@dataclass(slots=True)
class AuthTokens:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class LifecycleResult:
    success: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ResetFlowResult:
    success: bool
    message: str
    reset_token: Optional[str] = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SupportSummary:
    subject: str
    details: str
    locale: str = "en"
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_locale(value: Optional[str]) -> str:
    if not value:
        return "en"
    return value.strip().replace("_", "-").lower()


def compact_mapping(mapping: Optional[Mapping[str, Any]]) -> dict[str, Any]:
    if not mapping:
        return {}
    return {str(k): v for k, v in mapping.items() if v is not None}
