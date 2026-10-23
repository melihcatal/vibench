from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------
# Request models used when calling external APIs
# ---------------------------------------------------
class AuthorizationRequest(BaseModel):
    response_type: str = Field(..., description="Response type (e.g., 'code')")
    client_id: str = Field(..., description="OAuth client identifier")
    redirect_uri: str = Field(..., description="Where the IdP redirects after auth")
    scope: str = Field(..., description="Requested scopes, space‑separated")
    state: Optional[str] = Field(None, description="CSRF protection value")
    nonce: Optional[str] = Field(None, description="Opaque value for replay protection")
    code_challenge: Optional[str] = Field(None, description="PKCE challenge")
    code_challenge_method: Optional[str] = Field(
        None, description="PKCE method (e.g., 'S256')"
    )

    class Config:
        extra = "allow"


class TokenExchangeRequest(BaseModel):
    grant_type: str = Field(
        ..., description="Grant type ('authorization_code', 'refresh_token', etc.)"
    )
    code: Optional[str] = Field(None, description="Authorization code")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    redirect_uri: Optional[str] = Field(
        None, description="Redirect URI used in the auth request"
    )
    client_id: Optional[str] = Field(None, description="Client identifier")
    client_secret: Optional[str] = Field(None, description="Client secret")
    code_verifier: Optional[str] = Field(
        None, description="PKCE verifier for the original flow"
    )

    class Config:
        extra = "allow"


# ---------------------------------------------------
# Response models – normalized for internal use
# ---------------------------------------------------
class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Bearer token for API calls")
    token_type: str = Field(..., description="Typically 'Bearer'")
    expires_in: int = Field(..., description="Lifetime of the access token in seconds")
    refresh_token: Optional[str] = Field(
        None, description="Token to obtain new access tokens"
    )
    id_token: Optional[str] = Field(None, description="JWT containing user claims")
    scope: Optional[str] = Field(None, description="Granted scopes")

    class Config:
        extra = "allow"


class UserInfoResponse(BaseModel):
    sub: str = Field(..., description="Subject identifier")
    email: Optional[str] = Field(None, description="User's e‑mail address")
    email_verified: Optional[bool] = Field(
        None, description="Whether the e‑mail is verified"
    )
    name: Optional[str] = Field(None, description="Full name")
    given_name: Optional[str] = Field(None, description="Given name / first name")
    family_name: Optional[str] = Field(None, description="Family name / last name")
    picture: Optional[str] = Field(None, description="URL to profile picture")
    # Add any other provider‑specific fields you wish to keep

    class Config:
        extra = "allow"


# ---------------------------------------------------
# Normalization helpers
# ---------------------------------------------------
class NormalizedProfile(BaseModel):
    user_id: str = Field(..., description="Primary key for the user")
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    # Insert additional standardized fields here (e.g., locale, locale_formatted, etc.)

    class Config:
        extra = "allow"


def normalize_profile_from_oidc(claims: Dict[str, Any]) -> NormalizedProfile:
    """Convert a raw OIDC claims dict to the canonical NormalizedProfile.

    This central function can be imported by same‑scenario files that use
    different providers; each provider first extracts a dict of raw claims
    then passes it here for a single source of truth.
    """
    # Example mapping for IBM App ID responses (others can be added similarly)
    return NormalizedProfile(
        user_id=claims.get("sub"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
    )
