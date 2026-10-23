from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class OAuthTokenResponse:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    token_type: str
    expires_in: int
    expires_at: Optional[int] = None


@dataclass
class NormalizedProfileClaims:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    custom_claims: Optional[Dict[str, Any]] = None


@dataclass
class FederatedLoginEvent:
    event_id: str
    user_id: str
    provider: str
    timestamp: str
    claims: NormalizedProfileClaims
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
