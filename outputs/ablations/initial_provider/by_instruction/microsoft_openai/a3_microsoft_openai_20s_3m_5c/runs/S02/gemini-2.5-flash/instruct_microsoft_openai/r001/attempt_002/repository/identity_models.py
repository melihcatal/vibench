from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class UserProfileClaims:
    """
    A normalized representation of user profile claims from a federated identity provider.
    """
    provider: str
    subject: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}
