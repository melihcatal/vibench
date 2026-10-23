from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class AuthConfig:
    domain: str
    client_id: str
    client_secret: str
    redirect_uri: str


@dataclass
class Tokens:
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None


@dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    event_type: str
    user_id: Optional[str] = None
    success: bool = False


def normalize_claims(claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=str(claims.get("sub", "")),
        email=claims.get("email"),
        name=claims.get("name") or claims.get("preferred_username"),
    )
