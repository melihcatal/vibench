from dataclasses import dataclass
from typing import Optional


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    preferred_username: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None
    # Add more fields as needed based on OIDC claims


@dataclass
class AuditLogRecord:
    user_id: str
    event_type: str
    timestamp: str
    ip_address: str
    user_agent: str
    details: dict
