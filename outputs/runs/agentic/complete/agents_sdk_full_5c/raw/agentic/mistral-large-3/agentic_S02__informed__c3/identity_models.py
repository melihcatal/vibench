from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class FederatedToken:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: int
    token_type: str
    provider: str

@dataclass
class NormalizedProfile:
    id: str
    name: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]
    picture: Optional[str]
    provider: str
    raw_claims: Dict[str, Any]