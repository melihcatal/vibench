import dataclasses
import datetime
from typing import Optional, Dict, Any, List

@dataclasses.dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    ext_expires_in: Optional[int] = None

@dataclasses.dataclass
class UserClaims:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    preferred_username: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    updated_at: Optional[datetime.datetime] = None
    # Add other common claims as needed
    raw_claims: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class AuditRecord:
    event_time: datetime.datetime
    event_type: str
    user_id: str
    ip_address: str
    user_agent: str
    details: Dict[str, Any]

@dataclasses.dataclass
class ConsentAgreement:
    user_id: str
    client_id: str
    scopes_granted: List[str]
    agreement_time: datetime.datetime
    raw_consent_data: Optional[Dict[str, Any]] = None
