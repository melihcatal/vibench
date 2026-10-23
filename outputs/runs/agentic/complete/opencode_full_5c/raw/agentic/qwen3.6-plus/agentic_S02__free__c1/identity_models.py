import os
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone


@dataclass
class OAuthConfig:
    provider: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: str = ""
    authorize_url: str = ""
    token_url: str = ""
    userinfo_url: str = ""
    scopes: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    state: Optional[str] = None
    nonce: Optional[str] = None
    extra_params: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class TokenResponse:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class AuditEvent:
    event_id: str
    event_type: str
    timestamp: str
    user_sub: str
    provider: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status: str = "success"
    details: Dict[str, Any] = field(default_factory=dict)
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "AuditEvent":
        return AuditEvent(
            **{k: v for k, v in data.items() if k in AuditEvent.__dataclass_fields__}
        )


@dataclass
class ConsentTranslation:
    source_language: str
    target_language: str
    original_text: str
    translated_text: str
    consent_type: str = "general"
    provider: Optional[str] = None


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    categories: Dict[str, float] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    provider: str = ""
    model: str = ""


def normalize_okta_claims(raw_claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        email_verified=raw_claims.get("email_verified", False),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=raw_claims.get("picture"),
        locale=raw_claims.get("locale"),
        provider="okta",
        raw_claims=raw_claims,
    )


def normalize_auth0_claims(raw_claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        email_verified=raw_claims.get("email_verified", False),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=raw_claims.get("picture"),
        locale=raw_claims.get("locale"),
        provider="auth0",
        raw_claims=raw_claims,
    )


def normalize_google_claims(raw_claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        email_verified=raw_claims.get("email_verified", False),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=raw_claims.get("picture"),
        locale=raw_claims.get("locale"),
        provider="google",
        raw_claims=raw_claims,
    )


def normalize_azure_claims(raw_claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=raw_claims.get("oid", raw_claims.get("sub", "")),
        email=raw_claims.get("email") or raw_claims.get("unique_name"),
        email_verified=raw_claims.get("email_verified", False),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=None,
        locale=raw_claims.get("locale"),
        provider="azure_ad",
        raw_claims=raw_claims,
    )


def generate_state() -> str:
    import secrets

    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    import secrets

    return secrets.token_urlsafe(32)


def build_audit_event(
    event_type: str,
    user_sub: str,
    provider: str,
    status: str = "success",
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    session_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> AuditEvent:
    import uuid

    return AuditEvent(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        timestamp=datetime.now(timezone.utc).isoformat(),
        user_sub=user_sub,
        provider=provider,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status,
        details=details or {},
        session_id=session_id,
    )


def serialize_audit_events(events: List[AuditEvent]) -> List[Dict[str, Any]]:
    return [e.to_dict() for e in events]


def deserialize_audit_events(data: List[Dict[str, Any]]) -> List[AuditEvent]:
    return [AuditEvent.from_dict(d) for d in data]
