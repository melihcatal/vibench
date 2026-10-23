from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class OAuthAuthorizationRequest:
    redirect_uri: str
    state: str
    nonce: str
    scope: str = "openid profile email"
    response_type: str = "code"
    extra_params: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class TokenExchangeRequest:
    code: str
    redirect_uri: str
    code_verifier: Optional[str] = None


@dataclass(frozen=True)
class FederatedUserProfile:
    subject: str
    display_name: str
    email: Optional[str] = None
    email_verified: bool = False
    issuer: Optional[str] = None
    raw_claims: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    subject: str
    actor: Optional[str]
    success: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ConsentTranslationRequest:
    text: str
    target_language: str


@dataclass(frozen=True)
class ModerationRequest:
    text: str
    category: str = "identity-notes"


@dataclass(frozen=True)
class StoredAuditRecord:
    id: str
    payload: Dict[str, Any]


def normalize_claims(claims: Mapping[str, Any]) -> FederatedUserProfile:
    subject = str(claims.get("sub") or claims.get("oid") or claims.get("user_id") or "")
    display_name = str(
        claims.get("name")
        or claims.get("preferred_username")
        or claims.get("given_name")
        or claims.get("email")
        or subject
    )
    email = claims.get("email")
    email_verified = bool(claims.get("email_verified", False))
    issuer = claims.get("iss")
    return FederatedUserProfile(
        subject=subject,
        display_name=display_name,
        email=str(email) if email is not None else None,
        email_verified=email_verified,
        issuer=str(issuer) if issuer is not None else None,
        raw_claims=dict(claims),
    )
