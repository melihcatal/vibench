"""
Local request, response, and normalization helpers for Federated Login Flow.

Provides data models for Auth0 OIDC tokens, user profile claims,
and normalization utilities for mapping provider-specific claims
to a standardized internal format.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AuthorizationRequest:
    """Request model for starting an OAuth/OIDC authorization flow."""

    state: str
    nonce: str
    redirect_uri: str
    scope: str
    response_type: str = "code"
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    connection: Optional[str] = None
    extra_params: dict[str, str] = field(default_factory=dict)


@dataclass
class CallbackRequest:
    """Request model for processing an OAuth callback."""

    code: str
    state: str
    expected_state: str
    redirect_uri: str
    code_verifier: Optional[str] = None


@dataclass
class TokenResponse:
    """Response model for token exchange."""

    access_token: str
    token_type: str = "Bearer"
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: int = 3600
    scope: str = ""
    raw_response: dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        return False

    @property
    def expires_at(self) -> float:
        return time.time() + self.expires_in


@dataclass
class UserProfile:
    """Normalized federated user profile."""

    subject: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    nickname: Optional[str] = None
    locale: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    raw_claims: dict[str, Any] = field(default_factory=dict)


class ClaimNormalizer:
    """Normalizes claims from Auth0 OIDC responses to a standard format."""

    @staticmethod
    def normalize(raw_claims: dict[str, Any]) -> UserProfile:
        """Normalize Auth0 OIDC claims to a UserProfile."""
        sub = raw_claims.get("sub", "")
        provider, provider_id = _parse_sub(sub)

        name = raw_claims.get("name", "")
        given_name = raw_claims.get("given_name", "")
        family_name = raw_claims.get("family_name", "")

        if not name and (given_name or family_name):
            name = f"{given_name} {family_name}".strip()

        return UserProfile(
            subject=sub,
            email=raw_claims.get("email"),
            email_verified=raw_claims.get("email_verified", False),
            name=name or None,
            given_name=given_name or None,
            family_name=family_name or None,
            picture=raw_claims.get("picture"),
            nickname=raw_claims.get("nickname"),
            locale=raw_claims.get("locale"),
            provider=provider,
            provider_id=provider_id,
            raw_claims=raw_claims,
        )


class TokenParser:
    """Parses token responses from Auth0."""

    @staticmethod
    def parse(raw: dict[str, Any]) -> TokenResponse:
        """Parse a token response dict into a TokenResponse."""
        return TokenResponse(
            access_token=raw["access_token"],
            token_type=raw.get("token_type", "Bearer"),
            id_token=raw.get("id_token"),
            refresh_token=raw.get("refresh_token"),
            expires_in=raw.get("expires_in", 3600),
            scope=raw.get("scope", ""),
            raw_response=raw,
        )


def _parse_sub(sub: str) -> tuple[str, str]:
    """Parse the 'sub' claim to extract provider and provider ID.

    Auth0 sub format: 'auth0|<user_id>' or '<provider>|<user_id>'
    e.g., 'google-oauth2|123456789', 'auth0|abcdef123456'
    """
    if "|" in sub:
        parts = sub.split("|", 1)
        return parts[0], parts[1]
    return "unknown", sub
