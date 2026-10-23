"""
Local request, response, and normalization helpers for Federated Login Flow.
Defines data models for OAuth tokens, user profiles, and audit events.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import json
import re


@dataclass
class TokenResponse:
    """Normalized token response from OAuth2 provider."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: str = ""

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=int(data.get("expires_in", 3600)),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope", ""),
        )


@dataclass
class FederatedProfile:
    """Normalized federated user profile."""
    sub: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    provider: str = "auth0"
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_userinfo(cls, data: Dict[str, Any]) -> "FederatedProfile":
        return cls(
            sub=data.get("sub", ""),
            email=data.get("email"),
            email_verified=data.get("email_verified", False),
            name=data.get("name"),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            picture=data.get("picture"),
            locale=data.get("locale"),
            updated_at=data.get("updated_at"),
            provider="auth0",
            raw_claims={k: v for k, v in data.items()},
        )


@dataclass
class LoginAuditEvent:
    """Audit event for federated login activity."""
    event_id: str
    event_type: str
    user_sub: str
    timestamp: str
    provider: str = "auth0"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    success: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


@dataclass
class AuditSummary:
    """Summary of federated login audit events."""
    total_events: int = 0
    successful_logins: int = 0
    failed_logins: int = 0
    unique_users: int = 0
    providers: Dict[str, int] = field(default_factory=dict)
    events_by_hour: Dict[str, int] = field(default_factory=dict)
    error_summary: Dict[str, int] = field(default_factory=dict)


def normalize_email(email: Optional[str]) -> Optional[str]:
    """Normalize email address to lowercase and strip whitespace."""
    if not email:
        return None
    return email.lower().strip()


def extract_provider_from_sub(sub: str) -> str:
    """Extract provider identifier from Auth0-style sub claim."""
    if "|" in sub:
        return sub.split("|")[0]
    return "unknown"


def parse_iso_timestamp(ts: Optional[str]) -> Optional[datetime]:
    """Parse ISO 8601 timestamp string to datetime."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def redact_sensitive_fields(data: Dict[str, Any], fields: Optional[List[str]] = None) -> Dict[str, Any]:
    """Redact sensitive fields from a dictionary for audit logging."""
    sensitive = fields or ["access_token", "refresh_token", "id_token", "client_secret", "code_verifier"]
    result = {}
    for key, value in data.items():
        if key in sensitive:
            result[key] = "[REDACTED]"
        elif isinstance(value, dict):
            result[key] = redact_sensitive_fields(value, fields)
        else:
            result[key] = value
    return result


def validate_redirect_uri(uri: str, allowed_domains: Optional[List[str]] = None) -> bool:
    """Validate redirect URI against allowed domains."""
    try:
        parsed = urlparse(uri)
        if parsed.scheme not in ("http", "https"):
            return False
        if allowed_domains:
            return parsed.hostname in allowed_domains
        return True
    except Exception:
        return False
