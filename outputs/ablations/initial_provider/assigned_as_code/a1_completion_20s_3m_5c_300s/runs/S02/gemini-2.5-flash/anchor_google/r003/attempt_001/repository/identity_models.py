import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None


@dataclasses.dataclass
class UserProfile:
    sub: str  # Subject identifier
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None
    # Additional claims can be stored here
    additional_claims: Optional[Dict[str, Any]] = None
