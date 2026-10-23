from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class UserProfileClaims:
    """Represents normalized user profile claims."""
    sub: str  # Subject identifier
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    # Add any other common claims as needed
    raw_claims: Dict[str, Any] = field(default_factory=dict) # To store all raw claims

@dataclass
class TokenResponse:
    """Represents the response from a token endpoint."""
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    # Add other fields as they appear in the token response
    raw_response: Dict[str, Any] = field(default_factory=dict)
