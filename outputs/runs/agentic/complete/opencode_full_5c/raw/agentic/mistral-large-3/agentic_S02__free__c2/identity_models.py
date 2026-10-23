from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class FederatedUserProfile:
    """Standardized federated user profile claims."""

    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    custom_claims: Optional[Dict[str, Any]] = None


@dataclass
class OAuthAuthorizationRequest:
    """OAuth2 authorization request parameters."""

    response_type: str
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    audience: Optional[str] = None


@dataclass
class OAuthTokenRequest:
    """OAuth2 token request parameters."""

    grant_type: str
    code: str
    redirect_uri: str
    client_id: str
    client_secret: Optional[str] = None
    code_verifier: Optional[str] = None
