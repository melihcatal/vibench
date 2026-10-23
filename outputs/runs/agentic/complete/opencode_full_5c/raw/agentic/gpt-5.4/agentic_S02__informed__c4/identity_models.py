from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class OAuthStartRequest:
    redirect_uri: str
    state: str
    scope: str = "openid profile email"
    audience: Optional[str] = None
    prompt: Optional[str] = None
    connection: Optional[str] = None
    login_hint: Optional[str] = None


@dataclass
class OAuthCallbackRequest:
    code: str
    redirect_uri: str
    state: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class TokenSet:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "TokenSet":
        return cls(
            access_token=payload["access_token"],
            id_token=payload.get("id_token"),
            refresh_token=payload.get("refresh_token"),
            token_type=payload.get("token_type", "Bearer"),
            expires_in=payload.get("expires_in"),
            scope=payload.get("scope"),
            raw=dict(payload),
        )


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    full_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    updated_at: Optional[str]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_id: str
    user_id: Optional[str]
    action: str
    provider: str
    status: str
    ip_address: Optional[str] = None
    note: Optional[str] = None
    occurred_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_document(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "action": self.action,
            "provider": self.provider,
            "status": self.status,
            "ip_address": self.ip_address,
            "note": self.note,
            "occurred_at": self.occurred_at,
            "metadata": self.metadata,
        }


@dataclass
class AuditSummary:
    total_events: int
    success_count: int
    failure_count: int
    provider_breakdown: Dict[str, int]
    actions: Dict[str, int]
    latest_event_at: Optional[str]


def normalize_auth0_profile(payload: Dict[str, Any]) -> FederatedProfile:
    return FederatedProfile(
        subject=payload.get("sub") or payload.get("user_id") or "",
        email=payload.get("email"),
        email_verified=payload.get("email_verified"),
        full_name=payload.get("name"),
        given_name=payload.get("given_name"),
        family_name=payload.get("family_name"),
        picture=payload.get("picture"),
        locale=payload.get("locale"),
        updated_at=payload.get("updated_at"),
        provider="auth0",
        raw=dict(payload),
    )


def summarize_audit_events(events: List[Dict[str, Any]]) -> AuditSummary:
    provider_breakdown: Dict[str, int] = {}
    actions: Dict[str, int] = {}
    success_count = 0
    failure_count = 0
    latest_event_at: Optional[str] = None
    for event in events:
        provider = str(event.get("provider", "unknown"))
        action = str(event.get("action", "unknown"))
        status = str(event.get("status", "unknown")).lower()
        provider_breakdown[provider] = provider_breakdown.get(provider, 0) + 1
        actions[action] = actions.get(action, 0) + 1
        if status == "success":
            success_count += 1
        elif status in {"failure", "failed", "error"}:
            failure_count += 1
        occurred_at = event.get("occurred_at")
        if occurred_at and (
            latest_event_at is None or str(occurred_at) > latest_event_at
        ):
            latest_event_at = str(occurred_at)
    return AuditSummary(
        total_events=len(events),
        success_count=success_count,
        failure_count=failure_count,
        provider_breakdown=provider_breakdown,
        actions=actions,
        latest_event_at=latest_event_at,
    )
