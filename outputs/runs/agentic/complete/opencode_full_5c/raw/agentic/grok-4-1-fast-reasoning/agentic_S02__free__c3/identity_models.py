from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List, Tuple


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    auth_url: str
    token_url: str
    scopes: List[str]


@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class UserClaims:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None


def normalize_claims(raw_claims: Dict[str, Any]) -> UserClaims:
    return UserClaims(
        sub=raw_claims.get("sub", ""),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        email=raw_claims.get("email"),
        email_verified=raw_claims.get("email_verified"),
        picture=raw_claims.get("picture"),
    )


@dataclass
class AuditEvent:
    timestamp: str
    event_type: str
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    success: bool = False
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FreeTextClaim:
    user_id: str
    claim_text: str


@dataclass
class ConsentText:
    text: str
    source_language: str
