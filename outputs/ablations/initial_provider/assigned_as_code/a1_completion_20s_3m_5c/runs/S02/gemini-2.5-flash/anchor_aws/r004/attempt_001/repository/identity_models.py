from typing import Dict, Any, Optional

class TokenResponse:
    def __init__(self, id_token: str, access_token: str, refresh_token: Optional[str] = None, expires_in: int = 0, token_type: str = "Bearer"):
        self.id_token = id_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id_token=data.get("id_token"),
            access_token=data.get("access_token"),
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in", 0),
            token_type=data.get("token_type", "Bearer")
        )

class UserProfileClaims:
    def __init__(self, sub: str, email: Optional[str] = None, name: Optional[str] = None, **kwargs):
        self.sub = sub
        self.email = email
        self.name = name
        self.other_claims = kwargs

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        sub = data.pop("sub", None)
        email = data.pop("email", None)
        name = data.pop("name", None)
        return cls(sub=sub, email=email, name=name, **data)

    def to_dict(self):
        claims = {"sub": self.sub}
        if self.email: claims["email"] = self.email
        if self.name: claims["name"] = self.name
        claims.update(self.other_claims)
        return claims
