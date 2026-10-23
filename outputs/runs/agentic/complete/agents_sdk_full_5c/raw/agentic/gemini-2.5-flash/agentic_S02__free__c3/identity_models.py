from typing import Optional, Dict, Any

class TokenResponse:
    """
    Represents the token response from an OAuth/OIDC token endpoint.
    """
    def __init__(
        self, 
        access_token: Optional[str] = None,
        id_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        token_type: Optional[str] = None,
        expires_in: Optional[int] = None
    ):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expires_in = expires_in

    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
        }

class UserProfileClaims:
    """
    Represents normalized user profile claims obtained after federated login.
    """
    def __init__(
        self,
        sub: Optional[str] = None,
        name: Optional[str] = None,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        email: Optional[str] = None,
        email_verified: Optional[bool] = None,
        picture: Optional[str] = None,
        locale: Optional[str] = None,
        updated_at: Optional[str] = None,
        raw_claims: Optional[Dict[str, Any]] = None
    ):
        self.sub = sub
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.email = email
        self.email_verified = email_verified
        self.picture = picture
        self.locale = locale
        self.updated_at = updated_at
        self.raw_claims = raw_claims

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "email": self.email,
            "email_verified": self.email_verified,
            "picture": self.picture,
            "locale": self.locale,
            "updated_at": self.updated_at,
            "raw_claims": self.raw_claims,
        }
