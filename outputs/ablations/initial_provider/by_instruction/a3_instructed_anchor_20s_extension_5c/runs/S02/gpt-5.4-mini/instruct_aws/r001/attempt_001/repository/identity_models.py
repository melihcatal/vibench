from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LoginRequest:
    redirect_uri: str
    state: str
    scope: List[str]
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    issuer: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_claims(claims: Dict[str, Any]) -> FederatedProfile:
    subject = str(claims.get("sub") or claims.get("subject") or claims.get("id") or "")
    return FederatedProfile(
        subject=subject,
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        issuer=claims.get("iss"),
        raw=dict(claims),
    )
