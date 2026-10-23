from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


@dataclass(slots=True)
class OAuthStartRequest:
    redirect_uri: str
    scope: str = "openid profile email"
    audience: str | None = None
    state: str | None = None
    prompt: str | None = None


@dataclass(slots=True)
class OAuthStartResponse:
    authorization_url: str
    state: str
    nonce: str
    code_verifier: str | None = None
    code_challenge: str | None = None
    issuer: str | None = None


@dataclass(slots=True)
class TokenExchangeResponse:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None
    scope: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class NormalizedProfile:
    subject: str
    email: str | None = None
    email_verified: bool | None = None
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None
    locale: str | None = None
    updated_at: str | None = None
    provider: str = "auth0"
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditRecord:
    record_id: str
    event_type: str
    subject: str | None
    provider: str
    timestamp: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ModerationResult:
    allowed: bool
    flagged: bool
    risk_score: float
    categories: dict[str, float] = field(default_factory=dict)
    provider: str = "Perspective API"
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    detected_source_language: str | None
    target_language: str
    provider: str = "DeepL"
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditSummary:
    summary_text: str
    provider: str = "openai:gpt-4o-mini"
    raw: dict[str, Any] = field(default_factory=dict)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def coerce_bool(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    return bool(value)


def compact_dict(data: Mapping[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def model_dump(instance: Any) -> dict[str, Any]:
    if hasattr(instance, "__dataclass_fields__"):
        return asdict(instance)
    raise TypeError("Unsupported model instance")
