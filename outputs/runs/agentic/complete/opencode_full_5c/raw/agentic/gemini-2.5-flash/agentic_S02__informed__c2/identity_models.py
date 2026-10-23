import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    updated_at: Optional[str] = None
    # Add any other standard or custom claims you expect
    _extra_claims: Optional[Dict[str, Any]] = dataclasses.field(default_factory=dict)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return UserProfileClaims(
            sub=data.get("sub"),
            name=data.get("name"),
            email=data.get("email"),
            email_verified=data.get("email_verified"),
            picture=data.get("picture"),
            updated_at=data.get("updated_at"),
            _extra_claims={
                k: v
                for k, v in data.items()
                if k
                not in [
                    "sub",
                    "name",
                    "email",
                    "email_verified",
                    "picture",
                    "updated_at",
                ]
            },
        )

    def to_dict(self):
        data = {
            "sub": self.sub,
            "name": self.name,
            "email": self.email,
            "email_verified": self.email_verified,
            "picture": self.picture,
            "updated_at": self.updated_at,
        }
        data.update(self._extra_claims)
        return {k: v for k, v in data.items() if v is not None}
