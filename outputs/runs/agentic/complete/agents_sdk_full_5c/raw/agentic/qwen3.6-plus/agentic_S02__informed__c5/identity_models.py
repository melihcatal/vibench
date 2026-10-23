"""Local request, response, and normalization helpers for Federated Login Flow.

This module defines Pydantic models and normalization utilities for
OAuth/OIDC tokens, user profiles, and audit events in the Auth0 federation flow.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json


@dataclass
class TokenResponse:
    """Normalized OAuth2 token response from Auth0."""
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, response_json: Dict[str, Any]) -> "TokenResponse":
        """Create TokenResponse from Auth0 /oauth/token endpoint response."""
        return cls(
            access_token=response_json.get("access_token", ""),
            id_token=response_json.get("id_token"),
            refresh_token=response_json.get("refresh_token"),
            token_type=response_json.get("token_type", "Bearer"),
            expires_in=response_json.get("expires_in", 0),
            scope=response_json.get("scope", ""),
            raw_response=response_json,
        )


@dataclass
class UserProfile:
    """Normalized federated user profile from Auth0 /userinfo."""
    subject: str = ""
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    nickname: Optional[str] = None
    identities: List[Dict[str, Any]] = field(default_factory=list)
    updated_at: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_userinfo(cls, userinfo: Dict[str, Any]) -> "UserProfile":
        """Normalize Auth0 /userinfo response into a UserProfile."""
        return cls(
            subject=userinfo.get("sub", ""),
            email=userinfo.get("email"),
            email_verified=userinfo.get("email_verified", False),
            name=userinfo.get("name"),
            given_name=userinfo.get("given_name"),
            family_name=userinfo.get("family_name"),
            picture=userinfo.get("picture"),
            nickname=userinfo.get("nickname"),
            identities=userinfo.get("identities", []),
            updated_at=userinfo.get("updated_at"),
            raw_claims=userinfo,
        )


@dataclass
class AuditEvent:
    """Federated login audit event record."""
    event_id: str
    event_type: str
    timestamp: str
    user_subject: str
    client_id: str
    connection: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    error_description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert audit event to dictionary for storage."""
        return asdict(self)

    def to_json(self) -> str:
        """Serialize audit event to JSON string."""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditEvent":
        """Create AuditEvent from dictionary."""
        return cls(
            event_id=data.get("event_id", ""),
            event_type=data.get("event_type", ""),
            timestamp=data.get("timestamp", ""),
            user_subject=data.get("user_subject", ""),
            client_id=data.get("client_id", ""),
            connection=data.get("connection", ""),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            success=data.get("success", True),
            error_description=data.get("error_description"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class ClaimsModerationResult:
    """Result of content moderation on user claims."""
    claim_text: str
    is_safe: bool
    categories: List[str] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    details: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TranslatedConsentText:
    """Translated consent copy for identity provider."""
    source_text: str
    source_language: str
    target_language: str
    translated_text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
