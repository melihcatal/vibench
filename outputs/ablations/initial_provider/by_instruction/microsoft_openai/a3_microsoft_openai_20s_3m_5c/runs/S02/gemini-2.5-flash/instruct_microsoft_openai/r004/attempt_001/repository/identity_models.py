from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class UserProfile:
    """
    A normalized representation of a federated user's profile claims.
    """
    sub: str          # Subject identifier
    provider: str     # The identity provider (e.g., "google", "auth0", "microsoft")
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    picture: Optional[str] = None
    locale: Optional[str] = None
    # Any other claims that are common or useful across providers
    additional_claims: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TokenResponse:
    """
    A generic structure to hold OAuth/OIDC token response data.
    """
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict) # To store the original, raw response

def normalize_claims(provider: str, raw_claims: Dict[str, Any]) -> UserProfile:
    """
    Normalizes raw claims from various identity providers into a common UserProfile format.
    This is a simplified example; a real implementation would have more robust mapping.
    """
    sub = raw_claims.get("sub") or raw_claims.get("oid") or raw_claims.get("id")
    if not sub:
        raise ValueError("Could not determine 'sub' (subject identifier) from raw claims.")

    normalized_profile = UserProfile(
        sub=str(sub),
        provider=provider,
        name=raw_claims.get("name") or raw_claims.get("displayName"),
        given_name=raw_claims.get("given_name") or raw_claims.get("firstName"),
        family_name=raw_claims.get("family_name") or raw_claims.get("lastName"),
        email=raw_claims.get("email") or raw_claims.get("userPrincipalName"),
        email_verified=raw_claims.get("email_verified", False) or raw_claims.get("verified", False),
        picture=raw_claims.get("picture") or raw_claims.get("photo"),
        locale=raw_claims.get("locale"),
        additional_claims={
            k: v for k, v in raw_claims.items() if k not in [
                "sub", "oid", "id", "name", "displayName", "given_name", "firstName",
                "family_name", "lastName", "email", "userPrincipalName",
                "email_verified", "verified", "picture", "photo", "locale"
            ]
        }
    )
    return normalized_profile

if __name__ == "__main__":
    # Example usage for UserProfile
    google_raw_claims = {
        "sub": "12345",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "picture": "http://example.com/pic.jpg",
        "email_verified": True,
        "locale": "en",
        "gender": "male" # additional claim
    }
    google_profile = normalize_claims("google", google_raw_claims)
    print(f"Google Profile: {google_profile}")

    # Example usage for TokenResponse
    sample_token_response_dict = {
        "access_token": "abc.xyz.123",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": "def.uvw.456",
        "refresh_token": "ghi.rst.789",
        "scope": "openid profile email"
    }
    token_resp = TokenResponse(**sample_token_response_dict)
    print(f"Token Response: {token_resp}")
