from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class AuthorizationResponse:
    """Represents the response received from the authorization server."""
    code: str
    state: str
    scope: Optional[str] = None
    id_token: Optional[str] = None
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None

@dataclass
class UserProfile:
    """Represents a normalized user profile after federated login."""
    subject: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None

class ClaimNormalizer:
    """Helper for normalizing raw claims into a UserProfile."""
    @staticmethod
    def normalize(raw_claims: Dict[str, Any]) -> UserProfile:
        """
        Normalizes a dictionary of raw claims into a standardized UserProfile object.
        """
        subject = raw_claims.get("sub")
        if not subject:
            raise ValueError("Subject claim ('sub') is required in raw claims.")

        return UserProfile(
            subject=subject,
            email=raw_claims.get("email"),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture=raw_claims.get("picture"),
        )
