import dataclasses
from typing import Optional

@dataclasses.dataclass
class AuthorizationRequest:
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    code_challenge: str
    code_challenge_method: str

@dataclasses.dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None

@dataclasses.dataclass
class UserProfile:
    subject: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
