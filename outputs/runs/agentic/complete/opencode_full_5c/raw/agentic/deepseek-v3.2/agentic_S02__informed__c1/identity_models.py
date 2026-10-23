from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None

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
            "updated_at": self.updated_at,
        }


@dataclass
class OAuthTokens:
    id_token: str
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_token": self.id_token,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
        }


@dataclass
class LoginRequest:
    redirect_uri: str
    state: Optional[str] = None
    nonce: Optional[str] = None
    scope: str = "openid profile email"


@dataclass
class CallbackRequest:
    code: str
    state: str
    code_verifier: str
    redirect_uri: str


@dataclass
class AuthError:
    error: str
    error_description: Optional[str] = None
    state: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.error,
            "error_description": self.error_description,
            "state": self.state,
        }
