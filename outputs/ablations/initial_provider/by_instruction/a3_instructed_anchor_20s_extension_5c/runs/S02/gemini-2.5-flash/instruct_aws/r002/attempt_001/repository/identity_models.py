from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AuthCodeRequest:
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    response_type: str = "code"

@dataclass
class TokenExchangeRequest:
    code: str
    client_id: str
    redirect_uri: str
    grant_type: str = "authorization_code"
    client_secret: Optional[str] = None # For confidential clients
    code_verifier: Optional[str] = None # For PKCE clients

@dataclass
class UserProfile:
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    # Add other common claims as needed
    raw_claims: Dict[str, Any] = None

def normalize_claims(raw_claims: Dict[str, Any]) -> UserProfile:
    """
    Normalizes raw claims from an identity provider into a consistent UserProfile.
    Assumes 'sub' is always present and maps to user_id.
    """
    return UserProfile(
        user_id=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        name=raw_claims.get("name"),
        picture=raw_claims.get("picture"),
        locale=raw_claims.get("locale"),
        updated_at=raw_claims.get("updated_at"),
        raw_claims=raw_claims
    )
