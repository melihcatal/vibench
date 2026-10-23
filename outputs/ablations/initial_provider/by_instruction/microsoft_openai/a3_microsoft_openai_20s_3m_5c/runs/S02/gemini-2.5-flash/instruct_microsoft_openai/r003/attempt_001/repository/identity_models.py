import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class AuthCodeRequest:
    client_id: str
    redirect_uri: str
    scope: str
    response_type: str
    state: str
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None

@dataclasses.dataclass
class TokenExchangeRequest:
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    code: str
    grant_type: str
    code_verifier: Optional[str] = None

@dataclasses.dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None

@dataclasses.dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    # Add other common claims as needed
    raw_claims: Dict[str, Any] = dataclasses.field(default_factory=dict)
