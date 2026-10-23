from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class OAuthTokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None

@dataclass
class UserProfileClaims:
    sub: str  # Subject (user ID)
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PkceLoginRequest:
    redirect_uri: str
    code_challenge: str
    code_challenge_method: str = "S256"
    state: Optional[str] = None
    scopes: list[str] = field(default_factory=lambda: ["openid", "profile", "email"])

@dataclass
class AuthorizationCodeExchangeRequest:
    code: str
    redirect_uri: str
    client_id: str
    client_secret: Optional[str] = None
    code_verifier: Optional[str] = None
