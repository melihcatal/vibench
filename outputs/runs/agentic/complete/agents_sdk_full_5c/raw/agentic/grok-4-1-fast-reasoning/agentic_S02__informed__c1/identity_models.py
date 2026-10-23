from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    token_type: str = 'Bearer'
    expires_in: int = 3600
    scope: str = ''
    refresh_token: Optional[str] = None

@dataclass
class UserClaims:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None

@dataclass
class AuditEvent:
    event_type: str
    timestamp: datetime
    client_id: str
    user_id: Optional[str] = None
    success: bool = True
