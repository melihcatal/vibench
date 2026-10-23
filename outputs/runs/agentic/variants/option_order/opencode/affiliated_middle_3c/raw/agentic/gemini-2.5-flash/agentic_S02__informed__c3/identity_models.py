import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class OAuthTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


@dataclasses.dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    federated_claims: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class AuditRecord:
    event_id: str
    timestamp: str
    event_type: str
    user_id: str
    ip_address: str
    details: Dict[str, Any]
