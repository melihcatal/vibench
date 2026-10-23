import dataclasses
from typing import Dict, Any, Optional


@dataclasses.dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 3600


@dataclasses.dataclass
class UserProfileClaims:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class AuditRecord:
    timestamp: str
    event_type: str
    user_id: str
    ip_address: str
    user_agent: str
    details: Dict[str, Any]
