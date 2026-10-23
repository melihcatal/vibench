"""
identity_models.py - Define local request, response, and normalization helpers
for Federated Login Flow.

Provides dataclasses and utilities for federated identity data structures.
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime


@dataclass
class OAuthRequest:
    """Request parameters for initiating an OAuth/OIDC login."""
    redirect_uri: str
    scope: str = "openid profile email"
    state: Optional[str] = None
    nonce: Optional[str] = None
    audience: Optional[str] = None
    prompt: Optional[str] = None
    max_age: Optional[int] = None
    extra_params: dict = field(default_factory=dict)


@dataclass
class TokenResponse:
    """Parsed OAuth token response."""
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: int = 3600
    token_type: str = "Bearer"
    scope: str = ""
    issued_at: Optional[float] = None


@dataclass
class FederatedUserProfile:
    """Normalized federated user profile across providers."""
    user_id: str = ""
    email: Optional[str] = None
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    upn: Optional[str] = None
    provider: str = ""
    authority: str = ""
    tenant_id: Optional[str] = None
    raw_claims: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary, excluding raw_claims by default."""
        return asdict(self)


@dataclass
class AuditEvent:
    """Federated login audit event record."""
    event_id: str
    event_type: str  # login_start, callback, token_exchange, profile_fetch, error
    user_id: Optional[str] = None
    provider: str = ""
    timestamp: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    state: Optional[str] = None
    error_message: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        if d.get("timestamp"):
            d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass
class LoginResult:
    """Final result of a federated login flow."""
    success: bool
    user_profile: Optional[FederatedUserProfile] = None
    tokens: Optional[TokenResponse] = None
    error: Optional[str] = None
    audit_events: list[AuditEvent] = field(default_factory=list)


def normalize_auth0_claims(raw_claims: dict) -> FederatedUserProfile:
    """Normalize Auth0 ID token claims to FederatedUserProfile."""
    return FederatedUserProfile(
        user_id=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        display_name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        surname=raw_claims.get("family_name"),
        provider="auth0",
        authority=f"https://{raw_claims.get('iss', '').replace('https://', '')}",
        raw_claims=raw_claims,
    )


def normalize_entra_claims(raw_claims: dict) -> FederatedUserProfile:
    """Normalize Microsoft Entra ID claims to FederatedUserProfile."""
    return FederatedUserProfile(
        user_id=raw_claims.get("oid", ""),
        email=raw_claims.get("mail") or raw_claims.get("upn"),
        display_name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        surname=raw_claims.get("family_name"),
        upn=raw_claims.get("upn"),
        provider="microsoft_entra_id",
        tenant_id=raw_claims.get("tid"),
        authority=raw_claims.get("iss", ""),
        raw_claims=raw_claims,
    )


def normalize_cognito_claims(raw_claims: dict) -> FederatedUserProfile:
    """Normalize Amazon Cognito claims to FederatedUserProfile."""
    return FederatedUserProfile(
        user_id=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        display_name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        surname=raw_claims.get("family_name"),
        provider="amazon_cognito",
        authority=raw_claims.get("iss", ""),
        raw_claims=raw_claims,
    )


def claims_to_profile(raw_claims: dict, provider: str = "") -> FederatedUserProfile:
    """Auto-detect provider and normalize claims."""
    issuer = raw_claims.get("iss", "")
    if "auth0.com" in issuer or provider == "auth0":
        return normalize_auth0_claims(raw_claims)
    elif "login.microsoftonline.com" in issuer or provider == "microsoft_entra_id":
        return normalize_entra_claims(raw_claims)
    elif "cognito" in issuer.lower() or provider == "amazon_cognito":
        return normalize_cognito_claims(raw_claims)

    # Generic fallback
    return FederatedUserProfile(
        user_id=raw_claims.get("sub", raw_claims.get("user_id", "")),
        email=raw_claims.get("email"),
        display_name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        surname=raw_claims.get("family_name"),
        provider=provider or "unknown",
        authority=issuer,
        raw_claims=raw_claims,
    )
