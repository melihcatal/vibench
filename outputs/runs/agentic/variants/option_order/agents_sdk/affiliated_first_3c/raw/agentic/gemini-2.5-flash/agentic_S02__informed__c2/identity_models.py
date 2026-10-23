import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class AuthRequest:
    """Represents a generic authentication request."""
    redirect_uri: str
    state: Optional[str] = None
    nonce: Optional[str] = None

@dataclass
class AuthCallbackResponse:
    """Represents a generic response from an OAuth/OIDC callback."""
    code: str
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None

@dataclass
class TokenExchangeRequest:
    """
    Represents a request to exchange an authorization code for tokens.
    """
    client_id: str
    client_secret: Optional[str] = None
    code: str
    redirect_uri: str
    code_verifier: Optional[str] = None  # For PKCE
    grant_type: str = "authorization_code"

@dataclass
class TokenResponse:
    """Represents the tokens received after a successful exchange."""
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

@dataclass
class UserProfileClaims:
    """Normalized federated user profile claims."""
    federated_id: str
    display_name: Optional[str] = None
    email_address: Optional[str] = None
    profile_picture_url: Optional[str] = None
    preferred_language: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_raw_claims(cls, raw_claims: Dict[str, Any]):
        """
        Normalizes raw claims from an identity provider into UserProfileClaims.
        This is an example mapping for common OIDC claims.
        """
        return cls(
            federated_id=raw_claims.get("sub", "unknown"),
            display_name=raw_claims.get("name") or raw_claims.get("preferred_username"),
            email_address=raw_claims.get("email"),
            profile_picture_url=raw_claims.get("picture"),
            preferred_language=raw_claims.get("locale"),
            raw_claims=raw_claims
        )

@dataclass
class AuditRecord:
    """
    Represents an audit record for a federated login event.
    """
    event_id: str
    timestamp: str
    user_id: str
    event_type: str
    ip_address: str
    user_agent: str
    status: str # e.g., 'SUCCESS', 'FAILURE'
    details: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)
