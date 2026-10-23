from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class UserProfileClaims:
    """
    Represents normalized user profile claims from an identity provider.
    """
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    raw_profile: Optional[Dict[str, Any]] = None
