"""
Local request, response, and normalization helpers for Federated Login Flow.

Provides Pydantic models for OAuth/OIDC state management, token payloads,
profile claims, and audit records used throughout the federated login flow.
"""

import base64
import hashlib
import secrets
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class OAuthState:
    """Tracks a single OAuth authorization request."""

    state: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    nonce: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    redirect_uri: str = ""
    scopes: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OAuthState":
        return cls(
            state=data.get("state", secrets.token_urlsafe(32)),
            nonce=data.get("nonce", secrets.token_urlsafe(32)),
            redirect_uri=data.get("redirect_uri", ""),
            scopes=data.get("scopes", ["openid", "profile", "email"]),
            created_at=data.get("created_at", time.time()),
        )


@dataclass
class TokenResponse:
    """Normalized token response from an OAuth/OIDC provider."""

    access_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "id_token": self.id_token,
            "scope": self.scope,
        }

    @classmethod
    def from_provider_response(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=int(data.get("expires_in", 3600)),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope", ""),
            raw_response=data,
        )


@dataclass
class UserProfile:
    """Normalized federated user profile claims."""

    sub: str = ""
    email: str = ""
    email_verified: bool = False
    name: str = ""
    given_name: str = ""
    family_name: str = ""
    nickname: str = ""
    picture: str = ""
    locale: str = ""
    updated_at: Optional[int] = None
    provider: str = ""
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "nickname": self.nickname,
            "picture": self.picture,
            "locale": self.locale,
            "updated_at": self.updated_at,
            "provider": self.provider,
        }

    @classmethod
    def from_oidc_claims(cls, claims: Dict[str, Any], provider: str = "") -> "UserProfile":
        return cls(
            sub=claims.get("sub", ""),
            email=claims.get("email", ""),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name", ""),
            given_name=claims.get("given_name", ""),
            family_name=claims.get("family_name", ""),
            nickname=claims.get("nickname", ""),
            picture=claims.get("picture", ""),
            locale=claims.get("locale", ""),
            updated_at=claims.get("updated_at"),
            provider=provider,
            raw_claims=claims,
        )


@dataclass
class PkcePair:
    """PKCE code verifier and challenge pair."""

    code_verifier: str = field(default_factory=lambda: secrets.token_urlsafe(64))
    code_challenge: str = ""

    def __post_init__(self):
        if not self.code_challenge:
            self.code_challenge = self._derive_challenge(self.code_verifier)

    @staticmethod
    def _derive_challenge(verifier: str) -> str:
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")

    def to_dict(self) -> Dict[str, str]:
        return {
            "code_verifier": self.code_verifier,
            "code_challenge": self.code_challenge,
        }


@dataclass
class AuditEvent:
    """Represents a federated login audit event."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    event_type: str = ""  # e.g., "login_start", "token_exchange", "profile_fetch", "login_success", "login_failure"
    sub: str = ""
    email: str = ""
    provider: str = ""
    ip_address: str = ""
    user_agent: str = ""
    state: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "sub": self.sub,
            "email": self.email,
            "provider": self.provider,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "state": self.state,
            "details": self.details,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditEvent":
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            timestamp=data.get("timestamp", time.time()),
            event_type=data.get("event_type", ""),
            sub=data.get("sub", ""),
            email=data.get("email", ""),
            provider=data.get("provider", ""),
            ip_address=data.get("ip_address", ""),
            user_agent=data.get("user_agent", ""),
            state=data.get("state", ""),
            details=data.get("details", {}),
            notes=data.get("notes", ""),
        )
