from typing import Dict, Any, Optional


def normalize_claims(raw_claims: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes raw claims from an identity provider into a standardized format."""
    normalized = {
        "sub": raw_claims.get("sub") or raw_claims.get("oid"),  # Subject identifier
        "email": raw_claims.get("email") or raw_claims.get("upn"), # Email address
        "name": raw_claims.get("name") or raw_claims.get("displayName"), # Full name
        "given_name": raw_claims.get("given_name") or raw_claims.get("givenName"),
        "family_name": raw_claims.get("family_name") or raw_claims.get("surname"),
        "picture": raw_claims.get("picture"), # URL of the user's profile picture
        "locale": raw_claims.get("locale") or raw_claims.get("preferredLanguage"), # Locale
        "preferred_username": raw_claims.get("preferred_username"),
    }
    return {k: v for k, v in normalized.items() if v is not None}


class UserProfile:
    def __init__(self, claims: Dict[str, Any]):
        self.sub: str = claims.get("sub", "")
        self.email: Optional[str] = claims.get("email")
        self.name: Optional[str] = claims.get("name")
        self.given_name: Optional[str] = claims.get("given_name")
        self.family_name: Optional[str] = claims.get("family_name")
        self.picture: Optional[str] = claims.get("picture")
        self.locale: Optional[str] = claims.get("locale")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "email": self.email,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture,
            "locale": self.locale,
        }
