from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"


@dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    picture: Optional[str] = None
    locale: Optional[str] = None

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
        }


@dataclass
class OAuthError:
    error: str
    error_description: Optional[str] = None
    error_uri: Optional[str] = None
