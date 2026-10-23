from dataclasses import dataclass
from typing import Optional

@dataclass
class NormalizedProfile:
    """
    A normalized user profile, abstracting over provider-specific claims.
    """
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    picture: Optional[str] = None
    raw_claims: Optional[dict] = None
