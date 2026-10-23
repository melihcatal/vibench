from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class OAuthStartResponse(BaseModel):
    """Response model for starting OAuth login."""

    authorization_url: str
    state: str
    code_verifier: Optional[str] = None


class OAuthCallbackResponse(BaseModel):
    """Response model for handling OAuth callback."""

    id_token: str
    access_token: str
    refresh_token: Optional[str] = None
    state: str


class ProfileClaims(BaseModel):
    """Normalized federated user profile claims."""

    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    preferred_username: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    iss: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None


class PKCELoginResponse(BaseModel):
    """Response model for PKCE login flow."""

    authorization_url: str
    state: str
    code_verifier: str
