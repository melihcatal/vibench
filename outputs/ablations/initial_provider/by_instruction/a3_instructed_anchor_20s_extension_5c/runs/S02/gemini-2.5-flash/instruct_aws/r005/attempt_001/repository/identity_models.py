import dataclasses
from typing import Optional

@dataclasses.dataclass
class OAuthTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"

@dataclasses.dataclass
class UserProfile:
    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    claims: dict = dataclasses.field(default_factory=dict)
