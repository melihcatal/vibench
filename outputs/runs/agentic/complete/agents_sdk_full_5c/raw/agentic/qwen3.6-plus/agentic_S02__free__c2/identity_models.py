"""
identity_models.py - Local request, response, and normalization helpers for Federated Login Flow

Provides Pydantic-like dataclasses for OAuth/OIDC flows,
PKCE flows, user profile normalization, and callback handling.
"""

import secrets
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict


def generate_state() -> str:
    """Generate a cryptographically secure OAuth state parameter."""
    return secrets.token_urlsafe(32)


# --- OAuth Login Models ---

@dataclass
class OAuthLoginRequest:
    """Represents an OAuth authorization request."""
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    nonce: str
    audience: Optional[str] = None
    connection: Optional[str] = None
    authorize_url: Optional[str] = None


@dataclass
class OAuthLoginResponse:
    """Response from starting an OAuth login flow."""
    success: bool
    authorization_url: Optional[str] = None
    state: Optional[str] = None
    nonce: Optional[str] = None
    login_request: Optional[OAuthLoginRequest] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# --- Token Exchange Models ---

@dataclass
class TokenExchangeRequest:
    """Represents a token exchange request."""
    code: str
    redirect_uri: str
    grant_type: str = "authorization_code"
    code_verifier: Optional[str] = None


@dataclass
class TokenExchangeResponse:
    """Response from exchanging an authorization code for tokens."""
    success: bool
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    exchange_request: Optional[TokenExchangeRequest] = None
    error: Optional[str] = None


# --- Callback Models ---

@dataclass
class CallbackResult:
    """Result of handling an OAuth callback."""
    success: bool
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    error: Optional[str] = None
    token_response: Optional[TokenExchangeResponse] = None


# --- PKCE Models ---

@dataclass
class PKCELoginRequest:
    """Represents a PKCE authorization request."""
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    code_verifier: str
    code_challenge: str
    code_challenge_method: str = "S256"
    audience: Optional[str] = None
    connection: Optional[str] = None
    authorize_url: Optional[str] = None


@dataclass
class PKCELoginResponse:
    """Response from starting a PKCE login flow."""
    success: bool
    authorization_url: Optional[str] = None
    state: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    login_request: Optional[PKCELoginRequest] = None
    error: Optional[str] = None


@dataclass
class PKCECallbackResult:
    """Result of handling a PKCE callback."""
    success: bool
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    code_verifier: Optional[str] = None
    error: Optional[str] = None
    token_response: Optional[TokenExchangeResponse] = None


# --- User Profile Models ---

@dataclass
class FederatedProfile:
    """Normalized federated user profile."""
    sub: str
    email: str
    email_verified: bool
    name: str
    given_name: str = ""
    family_name: str = ""
    picture_url: str = ""
    updated_at: str = ""
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedClaims:
    """Normalized claims from an identity provider."""
    profile: FederatedProfile
    idp_provider: str
    idp_connections: List[str] = field(default_factory=list)
    all_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserProfileResponse:
    """Response from fetching and normalizing user profile."""
    success: bool
    normalized_claims: Optional[NormalizedClaims] = None
    error: Optional[str] = None
