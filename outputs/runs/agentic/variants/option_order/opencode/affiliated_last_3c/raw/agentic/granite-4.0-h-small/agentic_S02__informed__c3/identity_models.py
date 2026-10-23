import os
from dataclasses import dataclass
from typing import TypedDict, Literal

# User profile claims normalized across providers


class ProviderClaim(TypedDict):
    sub: str  # subject identifier
    email: str | None
    email_verified: bool | None
    name: str | None
    picture: str | None
    locale: str | None


# Auth0 token response model (used in same-scenario example)
@dataclass
class Auth0TokenResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None


# OIDC token response common fields (used for Google)
@dataclass
class OIDCTokenResponse:
    id_token: str
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None


# Audit event severity levels
@dataclass
class AuditEvent:
    event_id: str
    description: str
    severity: Literal["critical", "high", "medium", "low"]
    timestamp: str
    metadata: dict | None = None


# Audited consent details
@dataclass
class ConsentAudit:
    consent_id: str
    scopes: list[str]
    user_id: str
    provider: str
    timestamp: str


# Normalized user claim structure used after profile fetch
@dataclass
class ProviderUserClaim(ProviderClaim):
    pass


# Token exchange request for PKCE flow
@dataclass
class PKCETokenExchangeRequest:
    grant_type: Literal["authorization_code"]
    client_id: str
    code: str
    redirect_uri: str
    code_verifier: str


# Token exchange request for authorization code flow (non‑PKCE)
@dataclass
class OAuthAuthorizationCodeRequest:
    grant_type: Literal["authorization_code"]
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str


# Normalized consent translation output
@dataclass
class ConsentTranslation:
    locale: str
    original: str
    translated: str
