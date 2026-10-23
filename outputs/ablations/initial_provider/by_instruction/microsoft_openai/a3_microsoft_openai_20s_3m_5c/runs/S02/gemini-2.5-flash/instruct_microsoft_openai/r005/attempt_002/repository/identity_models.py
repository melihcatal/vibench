
import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class OAuthTokens:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    id_token: Optional[str] = None

@dataclasses.dataclass
class UserProfile:
    id: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    raw_claims: Dict[str, Any] = dataclasses.field(default_factory=dict)
