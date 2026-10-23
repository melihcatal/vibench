from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class AuthTokens:
    id_token: str
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None

@dataclass
class UserClaims:
    sub: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    preferred_username: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.name and (self.given_name or self.family_name):
            self.name = f"{self.given_name or ''} {self.family_name or ''}".strip()


@dataclass
class PKCECodePair:
    code_verifier: str
    code_challenge: str
