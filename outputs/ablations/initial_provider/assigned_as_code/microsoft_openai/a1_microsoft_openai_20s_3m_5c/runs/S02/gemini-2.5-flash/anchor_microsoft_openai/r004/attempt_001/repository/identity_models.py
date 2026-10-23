import json
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class OAuthTokenResponse:
    access_token: str
    expires_in: int
    scope: str
    token_type: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None

@dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    # Add any other common claims

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfileClaims':
        return cls(
            sub=data.get("sub"),
            name=data.get("name"),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            email=data.get("email"),
            email_verified=data.get("email_verified"),
            picture=data.get("picture"),
            locale=data.get("locale"),
        )

@dataclass
class PkceCodeVerifier:
    code_verifier: str
    code_challenge: str
    code_challenge_method: str = "S256"

@dataclass
class AuditRecord:
    timestamp: str
    event_type: str
    user_id: str
    details: Dict[str, Any] = field(default_factory=dict)
