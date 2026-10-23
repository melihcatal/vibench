
"""
Define local request, response, and normalization helpers for Federated Login Flow.
"""

from typing import Dict, Any, Optional

class FederatedLoginRequest:
    """Represents a request for a federated login."""
    def __init__(self, provider: str, redirect_uri: str, state: Optional[str] = None):
        self.provider = provider
        self.redirect_uri = redirect_uri
        self.state = state

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "redirect_uri": self.redirect_uri,
            "state": self.state
        }

class FederatedLoginResponse:
    """Represents a response from a federated login."""
    def __init__(self, code: str, state: Optional[str] = None, id_token: Optional[str] = None):
        self.code = code
        self.state = state
        self.id_token = id_token

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FederatedLoginResponse":
        return cls(
            code=data.get("code"),
            state=data.get("state"),
            id_token=data.get("id_token")
        )

class NormalizedUserProfile:
    """Represents a normalized user profile after federated login."""
    def __init__(self, user_id: str, email: str, display_name: Optional[str] = None,
                 first_name: Optional[str] = None, last_name: Optional[str] = None,
                 raw_claims: Optional[Dict[str, Any]] = None):
        self.user_id = user_id
        self.email = email
        self.display_name = display_name
        self.first_name = first_name
        self.last_name = last_name
        self.raw_claims = raw_claims

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "display_name": self.display_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "raw_claims": self.raw_claims
        }

def normalize_claims(raw_claims: Dict[str, Any]) -> NormalizedUserProfile:
    """
    Normalizes raw claims from an identity provider into a standard user profile.
    This is a placeholder function and should be implemented based on specific IDP claims.
    """
    user_id = raw_claims.get("sub") or raw_claims.get("id") or "unknown_id"
    email = raw_claims.get("email") or "unknown_email"
    display_name = raw_claims.get("name")
    first_name = raw_claims.get("given_name")
    last_name = raw_claims.get("family_name")

    return NormalizedUserProfile(
        user_id=user_id,
        email=email,
        display_name=display_name,
        first_name=first_name,
        last_name=last_name,
        raw_claims=raw_claims
    )
