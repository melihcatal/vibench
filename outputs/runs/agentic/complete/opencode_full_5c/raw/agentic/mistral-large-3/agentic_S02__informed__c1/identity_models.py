from typing import Dict, Any, Optional
from pydantic import BaseModel


class OAuthTokenResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: Optional[str]
    expires_in: int
    token_type: str


class UserProfileClaims(BaseModel):
    sub: str
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]
    picture: Optional[str]
    locale: Optional[str]
    preferred_username: Optional[str]


class PKCEData(BaseModel):
    code_verifier: str
    code_challenge: str
    code_challenge_method: str = "S256"


class OAuthState(BaseModel):
    state: str
    redirect_uri: str
    nonce: Optional[str] = None
    pkce_data: Optional[PKCEData] = None
