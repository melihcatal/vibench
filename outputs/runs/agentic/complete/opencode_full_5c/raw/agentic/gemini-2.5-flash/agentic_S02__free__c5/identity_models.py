from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Tokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None


@dataclass
class UserProfile:
    sub: str  # Subject identifier
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    # Any other custom claims can be stored here
    custom_claims: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_auth0_claims(claims: Dict[str, Any]) -> "UserProfile":
        return UserProfile(
            sub=claims.get("sub"),
            name=claims.get("name"),
            email=claims.get("email"),
            email_verified=claims.get("email_verified"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            updated_at=claims.get("updated_at"),
            custom_claims={
                k: v
                for k, v in claims.items()
                if k
                not in [
                    "sub",
                    "name",
                    "email",
                    "email_verified",
                    "picture",
                    "locale",
                    "updated_at",
                ]
            },
        )


@dataclass
class FederatedLoginAuditRecord:
    event_id: str
    timestamp: str
    event_type: str
    user_id: str
    provider: str
    details: Dict[str, Any]
