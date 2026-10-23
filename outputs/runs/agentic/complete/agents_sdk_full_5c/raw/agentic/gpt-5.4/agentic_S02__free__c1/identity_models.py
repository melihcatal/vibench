from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class OAuthStartRequest:
    redirect_uri: str
    scope: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    state: Optional[str] = None
    prompt: Optional[str] = None
    login_hint: Optional[str] = None


@dataclass(slots=True)
class OAuthStartResponse:
    authorization_url: str
    state: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass(slots=True)
class TokenExchangeRequest:
    code: str
    redirect_uri: str
    code_verifier: Optional[str] = None


@dataclass(slots=True)
class TokenSet:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FederatedProfile:
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditEvent:
    event_type: str
    provider: str
    actor_subject: Optional[str]
    occurred_at: str
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def now(cls, event_type: str, provider: str, actor_subject: Optional[str], details: Optional[Dict[str, Any]] = None) -> "AuditEvent":
        return cls(
            event_type=event_type,
            provider=provider,
            actor_subject=actor_subject,
            occurred_at=datetime.now(timezone.utc).isoformat(),
            details=details or {},
        )


def normalize_scopes(scope_value: Any) -> List[str]:
    if scope_value is None:
        return []
    if isinstance(scope_value, str):
        return [item for item in scope_value.split() if item]
    if isinstance(scope_value, list):
        return [str(item) for item in scope_value]
    return [str(scope_value)]


def normalize_bool(value: Any) -> Optional[bool]:
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
