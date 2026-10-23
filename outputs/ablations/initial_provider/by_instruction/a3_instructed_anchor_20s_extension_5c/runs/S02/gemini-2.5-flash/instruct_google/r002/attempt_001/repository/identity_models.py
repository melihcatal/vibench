from typing import Dict, Any, Optional

class OAuthTokenResponse:
    def __init__(self, data: Dict[str, Any]):
        self.access_token = data.get("access_token")
        self.expires_in = data.get("expires_in")
        self.scope = data.get("scope")
        self.token_type = data.get("token_type")
        self.id_token = data.get("id_token")
        self.refresh_token = data.get("refresh_token")

class UserProfileClaims:
    def __init__(self, raw_claims: Dict[str, Any]):
        self.sub: Optional[str] = raw_claims.get("sub")
        self.email: Optional[str] = raw_claims.get("email")
        self.email_verified: Optional[bool] = raw_claims.get("email_verified")
        self.name: Optional[str] = raw_claims.get("name")
        self.given_name: Optional[str] = raw_claims.get("given_name")
        self.family_name: Optional[str] = raw_claims.get("family_name")
        self.picture: Optional[str] = raw_claims.get("picture")
        self.locale: Optional[str] = raw_claims.get("locale")
        self._raw_claims = raw_claims

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture,
            "locale": self.locale,
        }

def normalize_claims(claims: Dict[str, Any]) -> UserProfileClaims:
    return UserProfileClaims(claims)
