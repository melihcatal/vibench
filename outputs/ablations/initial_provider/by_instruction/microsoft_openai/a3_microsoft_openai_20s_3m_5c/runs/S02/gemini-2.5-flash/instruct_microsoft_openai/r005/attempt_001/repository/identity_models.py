import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class OAuthState:
    session_id: str
    redirect_uri: str
    pkce_code_verifier: Optional[str] = None

@dataclasses.dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    token_type: str
    expires_in: int

@dataclasses.dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    preferred_username: Optional[str] = None
    claims: Dict[str, Any] = dataclasses.field(default_factory=dict)
