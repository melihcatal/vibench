from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import hashlib
import json


@dataclass
class OAuthStartRequest:
    redirect_uri: str
    state: str
    scopes: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    prompt: Optional[str] = None
    connection: Optional[str] = None
    audience: Optional[str] = None


@dataclass
class CallbackTokens:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedProfile:
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    updated_at: Optional[str]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditRecord:
    event_id: str
    event_type: str
    provider: str
    user_id: Optional[str]
    session_id: Optional[str]
    timestamp: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditSummary:
    provider: str
    total_events: int
    successful_logins: int
    failed_logins: int
    unique_users: int
    period_start: Optional[str]
    period_end: Optional[str]
    generated_text: str
    model: str


@dataclass
class ModerationResult:
    provider: str
    action: str
    flagged: bool
    scores: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    source_language: Optional[str]
    target_language: str
    translated_text: str
    raw: Dict[str, Any] = field(default_factory=dict)



def normalize_scopes(scope_value: Any) -> List[str]:
    if scope_value is None:
        return []
    if isinstance(scope_value, list):
        return [str(item) for item in scope_value if str(item).strip()]
    if isinstance(scope_value, str):
        return [part for part in scope_value.split() if part]
    return [str(scope_value)]



def normalize_auth0_profile(claims: Dict[str, Any]) -> NormalizedProfile:
    return NormalizedProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        updated_at=str(claims.get("updated_at")) if claims.get("updated_at") is not None else None,
        provider="Auth0",
        raw=claims,
    )



def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()



def stable_event_id(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
