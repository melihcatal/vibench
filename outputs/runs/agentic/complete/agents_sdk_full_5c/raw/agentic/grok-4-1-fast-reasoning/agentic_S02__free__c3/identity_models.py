from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List

@dataclass
class OAuthConfig:
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: str
    scopes: List[str]
    auth_url: str
    token_url: str
    userinfo_url: str

@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = 'Bearer'
    expires_in: int = 3600

@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None

def normalize_profile(claims: Dict[str, Any]) -&gt; UserProfile:
    return UserProfile(
        sub=claims.get('sub', ''),
        email=claims.get('email'),
        name=claims.get('name'),
        picture=claims.get('picture')
    )

@dataclass
class AuditEvent:
    event_type: str
    user_id: str
    timestamp: str
    details: Dict[str, Any]
