from pydantic import BaseModel, Field
from typing import Optional, Dict


class LoginEvent(BaseModel):
    user_id: str = Field(..., description='Unique identifier for the federated user')
    source: str = Field(..., description='Name of the identity provider (e.g., Microsoft Entra ID)')
    timestamp: str = Field(..., description='ISO 8601 timestamp when the login completed')
    claims: Dict[str, Optional[str]] = Field(..., description='Raw OIDC claims received from the provider')


class UserProfile(BaseModel):
    user_id: str = Field(..., description='Primary key matching LoginEvent.user_id')
    username: str = Field(..., description='Display name or preferred username')
    email: Optional[str] = Field(None, description='Verified email address')
    given_name: Optional[str] = Field(None, description='First name')
    family_name: Optional[str] = Field(None, description='Last name')
    picture: Optional[str] = Field(None, description='URL of profile picture')
    locale: Optional[str] = Field(None, description='Locale code (e.g., en-US)')


class AuthTokenSet(BaseModel):
    access_token: str = Field(..., description='Bearer token for API calls')
    id_token: str = Field(..., description='JWT containing user identity claims')
    refresh_token: Optional[str] = Field(None, description='Long‑lived token for refreshing access')
    expires_at: float = Field(..., description='Unix epoch time when the access token expires')


class NormalizedClaims(BaseModel):
    sub: str = Field(..., description='OIDC subject identifier')
    name: Optional[str] = None
    preferred_username: Optional[str] = None
    email: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    # Add any additional standard claims as needed
