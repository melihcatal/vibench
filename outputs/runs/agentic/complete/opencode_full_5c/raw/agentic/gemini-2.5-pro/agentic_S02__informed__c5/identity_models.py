from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None


@dataclass
class NormalizedProfile:
    id: str
    email: str
    name: str
    nickname: Optional[str] = None
    picture: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None


@dataclass
class AuditEvent:
    event_id: str
    user_id: str
    event_type: str
    timestamp: str
    details: Dict[str, Any]
