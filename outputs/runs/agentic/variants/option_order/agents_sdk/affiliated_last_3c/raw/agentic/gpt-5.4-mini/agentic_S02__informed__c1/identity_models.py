from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping


@dataclass
class AuthorizationRequest:
    authorization_endpoint: str
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    response_type: str = "code"
    state: str = ""
    nonce: str = ""
    code_challenge: str = ""
    code_challenge_method: str = "S256"


@dataclass
class TokenResponse:
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = ""
    expires_in: int = 0
    scope: str = ""
    raw: dict[str, Any] | None = None


@dataclass
class FederatedProfile:
    subject: str
    email: str = ""
    email_verified: bool = False
    display_name: str = ""
    given_name: str = ""
    family_name: str = ""
    picture: str = ""
    issuer: str = ""
    raw: dict[str, Any] | None = None


@dataclass
class AuditEvent:
    event_type: str
    provider: str
    subject: str
    timestamp: str
    details: dict[str, Any]


def normalize_profile_claims(claims: Mapping[str, Any]) -> FederatedProfile:
    subject = str(claims.get("sub") or claims.get("user_id") or claims.get("oid") or "")
    email = str(claims.get("email") or claims.get("upn") or "")
    display_name = str(claims.get("name") or claims.get("preferred_username") or email)
    given_name = str(claims.get("given_name") or "")
    family_name = str(claims.get("family_name") or "")
    picture = str(claims.get("picture") or claims.get("avatar_url") or "")
    issuer = str(claims.get("iss") or claims.get("issuer") or "")
    email_verified = bool(claims.get("email_verified", False))
    return FederatedProfile(
        subject=subject,
        email=email,
        email_verified=email_verified,
        display_name=display_name,
        given_name=given_name,
        family_name=family_name,
        picture=picture,
        issuer=issuer,
        raw=dict(claims),
    )


def dataclass_to_dict(obj: Any) -> dict[str, Any]:
    return asdict(obj)
