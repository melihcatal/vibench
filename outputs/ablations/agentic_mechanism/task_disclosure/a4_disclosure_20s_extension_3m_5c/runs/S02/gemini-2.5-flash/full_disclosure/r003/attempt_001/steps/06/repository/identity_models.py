
import json
from typing import Dict, Any, Optional

class FederatedLoginRequest:
    """Represents a request for a federated login flow."""
    def __init__(self, provider: str, redirect_uri: str, state: Optional[str] = None, nonce: Optional[str] = None):
        self.provider = provider  # e.g., "google", "auth0"
        self.redirect_uri = redirect_uri
        self.state = state
        self.nonce = nonce

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "redirect_uri": self.redirect_uri,
            "state": self.state,
            "nonce": self.nonce
        }

class FederatedLoginResponse:
    """Represents a response from a federated login flow."""
    def __init__(self, provider: str, code: str, state: Optional[str] = None):
        self.provider = provider
        self.code = code
        self.state = state

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FederatedLoginResponse':
        return cls(
            provider=data.get("provider", ""),
            code=data.get("code", ""),
            state=data.get("state")
        )

class UserProfileClaims:
    """Normalizes user profile claims from various identity providers."""
    def __init__(self, raw_claims: Dict[str, Any]):
        self._raw_claims = raw_claims
        self.sub = raw_claims.get("sub")
        self.email = raw_claims.get("email")
        self.email_verified = raw_claims.get("email_verified", False)
        self.name = raw_claims.get("name")
        self.given_name = raw_claims.get("given_name")
        self.family_name = raw_claims.get("family_name")
        self.picture = raw_claims.get("picture")
        self.locale = raw_claims.get("locale")

    def get_raw_claims(self) -> Dict[str, Any]:
        return self._raw_claims

    def to_json(self) -> str:
        return json.dumps({
            "sub": self.sub,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture,
            "locale": self.locale
        }, indent=2)

def normalize_claims(provider: str, claims: Dict[str, Any]) -> UserProfileClaims:
    """
    Normalizes claims from a specific identity provider into a common UserProfileClaims format.
    This is a placeholder for actual provider-specific normalization logic.
    """
    # Example: For a Google-like provider, claims might already be mostly OIDC standard
    # For other providers, more mapping logic would be needed here.
    # The 'provider' argument can be used to branch normalization logic.
    if provider == "google":
        # Google provides standard OIDC claims
        return UserProfileClaims(claims)
    elif provider == "auth0":
        # Auth0 might have slightly different claim names or structures
        # This is a simplification; in a real app, you'd map Auth0-specific claims
        mapped_claims = {
            "sub": claims.get("sub"),
            "email": claims.get("email"),
            "email_verified": claims.get("email_verified"),
            "name": claims.get("name"),
            "given_name": claims.get("given_name"),
            "family_name": claims.get("family_name"),
            "picture": claims.get("picture"),
            "locale": claims.get("locale"),
        }
        return UserProfileClaims(mapped_claims)
    else:
        # Default or generic mapping
        return UserProfileClaims(claims)
