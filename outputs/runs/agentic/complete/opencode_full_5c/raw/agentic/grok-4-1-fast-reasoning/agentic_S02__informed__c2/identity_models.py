from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional


@dataclass
class TokenResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None


@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None

    @classmethod
    def from_claims(cls, claims: Dict[str, Any]) -> "UserProfile":
        return cls(
            sub=claims.get("sub"),
            name=claims.get("name"),
            email=claims.get("email"),
            picture=claims.get("picture"),
        )


@dataclass
class AuditEvent:
    timestamp: str
    event_type: str
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    success: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
