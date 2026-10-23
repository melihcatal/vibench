import dataclasses
from typing import Dict, Any, Optional


@dataclasses.dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"


@dataclasses.dataclass
class UserProfile:
    sub: str  # Subject identifier
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    raw_claims: Dict[str, Any] = dataclasses.field(default_factory=dict)
