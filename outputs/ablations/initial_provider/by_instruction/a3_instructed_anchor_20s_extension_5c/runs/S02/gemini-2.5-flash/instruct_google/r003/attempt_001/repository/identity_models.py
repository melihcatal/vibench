from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class OAuthProviderConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    scope: List[str] = field(default_factory=list)

@dataclass
class AuthCodeExchangeRequest:
    code: str
    redirect_uri: str
    client_id: str
    client_secret: str
    code_verifier: Optional[str] = None

@dataclass
class TokenResponse:
    access_token: str
    expires_in: int
    token_type: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None

@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    email_verified: Optional[bool] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AuditRecord:
    event_type: str
    timestamp: str
    user_id: str
    details: Dict[str, Any] = field(default_factory=dict)
