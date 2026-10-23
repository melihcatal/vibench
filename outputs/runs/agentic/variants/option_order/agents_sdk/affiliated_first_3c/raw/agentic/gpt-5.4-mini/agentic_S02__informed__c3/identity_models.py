from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True)
class AuthorizationRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    response_type: str = "code"
    state: str = ""
    nonce: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"


@dataclass(slots=True)
class TokenExchangeRequest:
    issuer: str
    client_id: str
    client_secret: str | None = None
    code: str = ""
    redirect_uri: str = ""
    code_verifier: str = ""


@dataclass(slots=True)
class FederatedProfile:
    subject: str
    email: str = ""
    full_name: str = ""
    given_name: str = ""
    family_name: str = ""
    picture: str = ""
    issuer: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditRecord:
    event_type: str
    subject: str
    issuer: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ConsentText:
    source_locale: str
    target_locale: str
    text: str


@dataclass(slots=True)
class ModerationResult:
    flagged: bool
    score: float
    categories: dict[str, float] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TokenSet:
    access_token: str
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    raw: dict[str, Any] = field(default_factory=dict)


def normalize_profile_claims(claims: Mapping[str, Any], issuer: str = "") -> FederatedProfile:
    subject = str(claims.get("sub") or claims.get("user_id") or claims.get("oid") or "")
    email = str(claims.get("email") or claims.get("preferred_username") or "")
    given = str(claims.get("given_name") or claims.get("first_name") or "")
    family = str(claims.get("family_name") or claims.get("last_name") or "")
    full_name = str(claims.get("name") or " ".join(x for x in [given, family] if x).strip())
    picture = str(claims.get("picture") or claims.get("avatar_url") or "")
    return FederatedProfile(
        subject=subject,
        email=email,
        full_name=full_name,
        given_name=given,
        family_name=family,
        picture=picture,
        issuer=issuer or str(claims.get("iss") or ""),
        raw=dict(claims),
    )
