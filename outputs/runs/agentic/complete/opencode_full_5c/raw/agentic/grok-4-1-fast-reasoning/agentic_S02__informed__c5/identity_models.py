from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class OAuthConfig:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: str = "http://localhost:3000/callback"


@dataclass
class TokenResponse:
    access_token: str
    token_type: str = "Bearer"
    id_token: str
    expires_in: int
    refresh_token: Optional[str] = None


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None


@dataclass
class AuditEvent:
    id: str
    timestamp: str
    event_type: str
    client_id: str
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    success: bool = False
