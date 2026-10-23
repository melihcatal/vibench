"""
Local request, response, and normalization helpers for Federated Login Flow.

Provides dataclasses and utility functions for handling OAuth/OIDC
authorization requests, token responses, and user profile claims.
"""

import base64
import hashlib
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode


@dataclass
class OAuthAuthorizationRequest:
    """Represents an OAuth 2.0 authorization request."""
    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: str = "openid profile email"
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    audience: Optional[str] = None
    connection: Optional[str] = None
    prompt: Optional[str] = None

    def to_url(self, auth_endpoint: str) -> str:
        """Serialize the authorization request to a URL."""
        params: Dict[str, str] = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "scope": self.scope,
        }
        if self.state:
            params["state"] = self.state
        if self.nonce:
            params["nonce"] = self.nonce
        if self.code_challenge:
            params["code_challenge"] = self.code_challenge
        if self.code_challenge_method:
            params["code_challenge_method"] = self.code_challenge_method
        if self.audience:
            params["audience"] = self.audience
        if self.connection:
            params["connection"] = self.connection
        if self.prompt:
            params["prompt"] = self.prompt
        return f"{auth_endpoint}?{urlencode(params)}"


@dataclass
class TokenResponse:
    """Represents an OAuth 2.0 / OIDC token response."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserProfileClaims:
    """Normalized federated user profile claims."""
    sub: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: Optional[str] = None
    idp_name: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    custom_claims: Dict[str, Any] = field(default_factory=dict)
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    """Represents a federated login audit event."""
    event_id: str
    event_type: str
    timestamp: datetime
    user_id: str
    provider: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[str] = None
    success: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


def generate_state(length: int = 32) -> str:
    """Generate a cryptographically secure OAuth state parameter."""
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8").rstrip("=")


def generate_nonce(length: int = 32) -> str:
    """Generate a cryptographically secure OIDC nonce."""
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8").rstrip("=")


def generate_code_verifier(length: int = 64) -> str:
    """Generate a PKCE code verifier."""
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8").rstrip("=")


def generate_code_challenge(code_verifier: str) -> str:
    """Generate a PKCE code challenge from a code verifier using S256."""
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def normalize_claims(raw_claims: Dict[str, Any], provider: str = "generic") -> UserProfileClaims:
    """Normalize raw OIDC/OAuth claims into a standard UserProfileClaims object."""
    profile = UserProfileClaims(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        email_verified=raw_claims.get("email_verified", False),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=raw_claims.get("picture"),
        locale=raw_claims.get("locale"),
        provider=provider,
        idp_name=raw_claims.get("iss", provider),
        roles=raw_claims.get("roles", raw_claims.get(f"https://{provider}/roles", [])),
        raw_claims=raw_claims,
    )

    for key, value in raw_claims.items():
        if key not in (
            "sub", "email", "email_verified", "name", "given_name",
            "family_name", "picture", "locale", "iss", "aud", "exp",
            "iat", "auth_time", "nonce", "acr", "amr", "roles",
        ):
            profile.custom_claims[key] = value

    if isinstance(profile.roles, str):
        profile.roles = [profile.roles]

    return profile


def parse_callback_query(query_params: Dict[str, str]) -> Dict[str, Optional[str]]:
    """Parse OAuth callback query parameters and extract relevant fields."""
    return {
        "code": query_params.get("code"),
        "state": query_params.get("state"),
        "error": query_params.get("error"),
        "error_description": query_params.get("error_description"),
    }


def extract_id_token_claims(id_token: str) -> Dict[str, Any]:
    """Decode the payload of a JWT ID token without verification."""
    parts = id_token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    payload = parts[1]
    padded = payload + "=" * (4 - len(payload) % 4)
    decoded = base64.urlsafe_b64decode(padded)
    import json
    return json.loads(decoded)


def format_audit_event(event: AuditEvent) -> Dict[str, Any]:
    """Format an audit event for storage or transmission."""
    data = asdict(event)
    data["timestamp"] = event.timestamp.isoformat()
    return data
