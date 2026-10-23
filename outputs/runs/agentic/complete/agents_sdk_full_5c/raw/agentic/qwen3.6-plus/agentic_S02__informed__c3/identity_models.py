"""Define local request, response, and normalization helpers for Federated Login Flow."""

import os
import base64
import hashlib
import secrets
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode


def generate_pkce_pair() -> dict:
    """Generate a PKCE code_verifier and code_challenge pair."""
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("ascii")).digest())
        .rstrip(b"=")
        .decode("ascii")
    )
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }


def generate_state() -> str:
    """Generate a cryptographically secure state parameter."""
    return secrets.token_urlsafe(32)


@dataclass
class AuthRequest:
    """Parameters for initiating an OAuth/OIDC authorization request."""
    client_id: str
    redirect_uri: str
    scope: str
    response_type: str = "code"
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = "S256"
    prompt: Optional[str] = None

    def to_authorization_url(self, authorization_endpoint: str) -> str:
        """Build the full authorization URL from request parameters."""
        params: Dict[str, str] = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": self.response_type,
            "state": self.state or generate_state(),
        }
        if self.nonce:
            params["nonce"] = self.nonce
        if self.code_challenge:
            params["code_challenge"] = self.code_challenge
            params["code_challenge_method"] = self.code_challenge_method or "S256"
        if self.prompt:
            params["prompt"] = self.prompt
        query = urlencode(params)
        return f"{authorization_endpoint}?{query}"


@dataclass
class TokenExchangeRequest:
    """Parameters for exchanging an authorization code for tokens."""
    grant_type: str = "authorization_code"
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    code_verifier: Optional[str] = None

    def to_form_body(self) -> Dict[str, str]:
        """Serialize to application/x-www-form-urlencoded body."""
        body: Dict[str, str] = {
            "grant_type": self.grant_type,
        }
        if self.code:
            body["code"] = self.code
        if self.redirect_uri:
            body["redirect_uri"] = self.redirect_uri
        if self.client_id:
            body["client_id"] = self.client_id
        if self.client_secret:
            body["client_secret"] = self.client_secret
        if self.code_verifier:
            body["code_verifier"] = self.code_verifier
        return body


@dataclass
class TokenResponse:
    """Normalized token response from an OIDC provider."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenResponse":
        """Create a TokenResponse from a provider response dict."""
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope"),
            raw_response=data,
        )


@dataclass
class UserProfileClaims:
    """Normalized federated user profile claims."""
    sub: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    preferred_username: Optional[str] = None
    updated_at: Optional[int] = None
    provider: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None

    @classmethod
    def from_oidc_claims(cls, claims: Dict[str, Any], provider: str = "unknown") -> "UserProfileClaims":
        """Normalize raw OIDC claims into a standardized profile."""
        return cls(
            sub=claims.get("sub", ""),
            email=claims.get("email"),
            email_verified=claims.get("email_verified"),
            name=claims.get("name"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            preferred_username=claims.get("preferred_username"),
            updated_at=claims.get("updated_at"),
            provider=provider,
            raw_claims=claims,
        )


@dataclass
class AuditEvent:
    """A single federated-login audit event record."""
    event_type: str
    timestamp: float
    user_sub: Optional[str] = None
    client_id: Optional[str] = None
    provider: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    details: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

    def to_document(self) -> Dict[str, Any]:
        """Serialize the audit event for storage."""
        return {
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "user_sub": self.user_sub,
            "client_id": self.client_id,
            "provider": self.provider,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "success": self.success,
            "details": self.details,
            "session_id": self.session_id,
        }
