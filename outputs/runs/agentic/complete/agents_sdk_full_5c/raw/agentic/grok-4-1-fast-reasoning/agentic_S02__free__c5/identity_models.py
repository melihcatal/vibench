from dataclasses import dataclass, asdict
from typing import Dict, Any, List
import json

@dataclass
class TokenResponse:
    access_token: str
    id_token: str = None
    refresh_token: str = None
    token_type: str = 'Bearer'
    expires_in: int = 0

@dataclass
class UserInfo:
    sub: str
    name: str = None
    given_name: str = None
    family_name: str = None
    email: str = None
    email_verified: bool = False
    picture: str = None

def normalize_user_claims(raw: Dict[str, Any]) -> UserInfo:
    fields = {k: v for k, v in asdict(UserInfo()).items()}
    return UserInfo(**{k: raw.get(k, fields[k]) for k in fields})

@dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    user_id: str
    action: str
    ip: str = None
    success: bool = False

def audit_events_to_json(events: List[AuditEvent]) -> str:
    return json.dumps([asdict(e) for e in events])