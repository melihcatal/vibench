from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


class GrantType(str, Enum):
    AUTHORIZATION_CODE = "authorization_code"
    PKCE = "authorization_code_pkce"
    REFRESH_TOKEN = "refresh_token"


class AuditEventType(str, Enum):
    LOGIN_INITIATED = "login_initiated"
    CALLBACK_RECEIVED = "callback_received"
    TOKEN_EXCHANGED = "token_exchanged"
    PROFILE_FETCHED = "profile_fetched"
    CONSENT_GRANTED = "consent_granted"
    CONSENT_DENIED = "consent_denied"
    SESSION_REFRESHED = "session_refreshed"
    LOGOUT_INITIATED = "logout_initiated"


@dataclass
class OAuthConfig:
    provider: str = "auth0"
    domain: str = ""
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""
    audience: str = ""
    scope: str = "openid profile email"
    response_type: str = "code"
    connection: str = ""
    state_ttl_seconds: int = 300


@dataclass
class PKCEPair:
    code_verifier: str = ""
    code_challenge: str = ""
    challenge_method: str = "S256"


@dataclass
class AuthorizationRequest:
    url: str = ""
    state: str = ""
    nonce: str = ""
    code_verifier: str = ""
    code_challenge: str = ""
    pkce_enabled: bool = False
    created_at: float = field(default_factory=time.time)


@dataclass
class CallbackPayload:
    code: str = ""
    state: str = ""
    error: str = ""
    error_description: str = ""


@dataclass
class TokenResponse:
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""
    received_at: float = field(default_factory=time.time)


@dataclass
class NormalizedProfile:
    sub: str = ""
    email: str = ""
    email_verified: bool = False
    name: str = ""
    given_name: str = ""
    family_name: str = ""
    picture: str = ""
    locale: str = ""
    provider: str = ""
    provider_connection: str = ""
    raw_claims: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_id: str = ""
    event_type: str = ""
    timestamp: str = ""
    user_sub: str = ""
    client_id: str = ""
    ip_address: str = ""
    user_agent: str = ""
    connection: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditSummary:
    total_events: int = 0
    unique_users: int = 0
    event_type_counts: dict[str, int] = field(default_factory=dict)
    connection_counts: dict[str, int] = field(default_factory=dict)
    time_range_start: str = ""
    time_range_end: str = ""
    top_ips: list[dict[str, Any]] = field(default_factory=list)
    failed_logins: int = 0


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    return secrets.token_urlsafe(32)


def generate_pkce_pair() -> PKCEPair:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = (
        digest.replace(b"+", b"-").replace(b"/", b"_").rstrip(b"=").decode("ascii")
    )
    return PKCEPair(
        code_verifier=verifier,
        code_challenge=challenge,
        challenge_method="S256",
    )


def normalize_profile_claims(
    raw_claims: dict[str, Any], provider: str = "auth0", connection: str = ""
) -> NormalizedProfile:
    return NormalizedProfile(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email", ""),
        email_verified=raw_claims.get("email_verified", False),
        name=raw_claims.get("name", ""),
        given_name=raw_claims.get("given_name", ""),
        family_name=raw_claims.get("family_name", ""),
        picture=raw_claims.get("picture", ""),
        locale=raw_claims.get("locale", ""),
        provider=provider,
        provider_connection=connection
        or raw_claims.get("identities", [{}])[0].get("connection", "")
        if raw_claims.get("identities")
        else connection,
        raw_claims=raw_claims,
    )


def build_audit_event(
    event_type: AuditEventType,
    user_sub: str = "",
    client_id: str = "",
    ip_address: str = "",
    user_agent: str = "",
    connection: str = "",
    details: dict[str, Any] | None = None,
) -> AuditEvent:
    return AuditEvent(
        event_id=secrets.token_hex(16),
        event_type=event_type.value,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        user_sub=user_sub,
        client_id=client_id,
        ip_address=ip_address,
        user_agent=user_agent,
        connection=connection,
        details=details or {},
    )
