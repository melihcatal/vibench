"""
identity_models.py - Local request, response, and normalization helpers
for Federated Login Flow.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class AuthRequest:
    """Parameters for initiating a federated login."""
    redirect_uri: str
    scope: str = "openid profile email"
    connection: str | None = None
    audience: str | None = None
    prompt: str | None = None
    login_hint: str | None = None
    extra_params: dict[str, str] = field(default_factory=dict)


@dataclass
class CallbackRequest:
    """Parameters received at the OAuth callback endpoint."""
    code: str
    state: str
    error: str | None = None
    error_description: str | None = None


@dataclass
class TokenResponse:
    """Normalized OAuth token response."""
    access_token: str
    token_type: str = "Bearer"
    id_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    scope: str | None = None
    raw_response: dict = field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw: dict) -> TokenResponse:
        return cls(
            access_token=raw.get("access_token", ""),
            token_type=raw.get("token_type", "Bearer"),
            id_token=raw.get("id_token"),
            refresh_token=raw.get("refresh_token"),
            expires_in=raw.get("expires_in"),
            scope=raw.get("scope"),
            raw_response=raw,
        )


@dataclass
class UserProfile:
    """Normalized federated user profile claims."""
    subject: str = ""
    email: str | None = None
    email_verified: bool = False
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    nickname: str | None = None
    picture: str | None = None
    locale: str | None = None
    zoneinfo: str | None = None
    phone_number: str | None = None
    identities: list[dict[str, Any]] = field(default_factory=list)
    raw_claims: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_email(email: str | None) -> str | None:
    """Normalize and validate an email address."""
    if not email:
        return None
    email = email.strip().lower()
    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return email
    return None


def normalize_profile(claims: dict[str, Any]) -> UserProfile:
    """Normalize raw OIDC / Auth0 userinfo claims into a UserProfile."""
    raw = dict(claims)
    return UserProfile(
        subject=raw.get("sub", ""),
        email=normalize_email(raw.get("email")),
        email_verified=bool(raw.get("email_verified", False)),
        name=raw.get("name"),
        given_name=raw.get("given_name"),
        family_name=raw.get("family_name"),
        nickname=raw.get("nickname"),
        picture=raw.get("picture"),
        locale=raw.get("locale"),
        zoneinfo=raw.get("zoneinfo"),
        phone_number=raw.get("phone_number"),
        identities=raw.get("identities", []),
        raw_claims=raw,
    )


def build_audit_record(
    event_type: str,
    subject: str | None = None,
    email: str | None = None,
    provider: str = "auth0",
    client_id: str | None = None,
    connection: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    metadata: dict | None = None,
    timestamp: datetime | None = None,
    details: str | None = None,
) -> dict:
    """Build a structured audit record dict."""
    return {
        "event_type": event_type,
        "subject": subject,
        "email": email,
        "provider": provider,
        "client_id": client_id,
        "connection": connection,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "metadata": metadata or {},
        "timestamp": (timestamp or datetime.now(timezone.utc)).isoformat(),
        "details": details,
    }
