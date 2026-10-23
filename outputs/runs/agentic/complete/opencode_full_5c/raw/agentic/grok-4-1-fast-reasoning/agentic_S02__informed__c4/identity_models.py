from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    preferred_username: Optional[str] = None


@dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    user_id: str
    action: str
    provider: str = "Microsoft Entra ID"
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
