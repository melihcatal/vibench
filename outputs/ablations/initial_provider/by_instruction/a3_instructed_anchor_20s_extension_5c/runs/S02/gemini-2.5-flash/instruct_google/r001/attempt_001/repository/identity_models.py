from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class UserProfileClaims:
    sub: str
    email: str
    email_verified: bool
    name: str
    given_name: str
    family_name: str
    picture: str
    locale: str
    raw_claims: Dict[str, Any] = field(default_factory=dict)
