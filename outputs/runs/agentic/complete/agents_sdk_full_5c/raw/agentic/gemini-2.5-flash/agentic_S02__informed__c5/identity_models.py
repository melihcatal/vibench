from typing import Optional, Dict, Any

class AuthTokens:
    """Represents the tokens received from an OAuth/OIDC provider."""
    def __init__(self, access_token: str, id_token: Optional[str] = None, 
                 refresh_token: Optional[str] = None, expires_in: Optional[int] = None,
                 token_type: Optional[str] = None):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in"),
            token_type=data.get("token_type"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
        }

class UserProfileClaims:
    """Represents normalized user profile claims."""
    def __init__(self, sub: str, name: Optional[str] = None, 
                 email: Optional[str] = None, email_verified: Optional[bool] = None,
                 picture: Optional[str] = None, updated_at: Optional[str] = None,
                 raw_claims: Optional[Dict[str, Any]] = None):
        self.sub = sub
        self.name = name
        self.email = email
        self.email_verified = email_verified
        self.picture = picture
        self.updated_at = updated_at
        self.raw_claims = raw_claims if raw_claims is not None else {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            sub=data.get("sub", ""),
            name=data.get("name"),
            email=data.get("email"),
            email_verified=data.get("email_verified"),
            picture=data.get("picture"),
            updated_at=data.get("updated_at"),
            raw_claims=data, # Store the original claims as well
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "name": self.name,
            "email": self.email,
            "email_verified": self.email_verified,
            "picture": self.picture,
            "updated_at": self.updated_at,
            "raw_claims": self.raw_claims,
        }
