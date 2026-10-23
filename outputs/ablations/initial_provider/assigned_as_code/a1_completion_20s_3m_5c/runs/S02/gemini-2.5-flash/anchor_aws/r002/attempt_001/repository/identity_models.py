from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class FederatedLoginConfig:
    domain: str
    client_id: str
    client_secret: str
    redirect_uri: str
    audience: Optional[str] = None
    scope: str = "openid profile email"


@dataclass
class OAuthCallbackPayload:
    code: str
    state: str
    redirect_uri: str


@dataclass
class TokenExchangeResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str


@dataclass
class UserProfileClaims:
    sub: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    # Additional claims can be added here
    raw_claims: Dict[str, Any] = None


@dataclass
class PkceLoginConfig:
    domain: str
    client_id: str
    redirect_uri: str
    audience: Optional[str] = None
    scope: str = "openid profile email"


@dataclass
class AuditRecord:
    timestamp: str
    event_type: str
    user_id: str
    details: Dict[str, Any]


@dataclass
class ConsentText:
    language: str
    text: str
