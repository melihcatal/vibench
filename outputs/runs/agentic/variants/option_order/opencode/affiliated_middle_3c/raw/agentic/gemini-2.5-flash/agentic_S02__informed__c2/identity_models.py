from pydantic import BaseModel
from typing import Optional, Dict, Any


class OAuthLoginRequest(BaseModel):
    redirect_uri: str
    scope: str = "openid profile email"
    audience: Optional[str] = None


class OAuthCallbackRequest(BaseModel):
    code: str
    state: str
    redirect_uri: str


class TokenResponse(BaseModel):
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str


class UserProfileClaims(BaseModel):
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    federated_provider: Optional[str] = "Auth0"
    raw_claims: Dict[str, Any]
