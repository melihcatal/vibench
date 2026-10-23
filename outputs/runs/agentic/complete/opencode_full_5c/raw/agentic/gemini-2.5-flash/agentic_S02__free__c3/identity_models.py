from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class UserProfile:
    provider: str
    sub: str  # Subject identifier
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    # Add any other common claims you expect


@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


def normalize_claims(provider: str, raw_claims: Dict[str, Any]) -> UserProfile:
    """
    Normalizes raw claims from different providers into a common UserProfile structure.
    """
    if provider == "google":
        return UserProfile(
            provider="google",
            sub=raw_claims.get("sub", ""),
            email=raw_claims.get("email"),
            email_verified=raw_claims.get("email_verified"),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture=raw_claims.get("picture"),
            locale=raw_claims.get("locale"),
        )
    elif provider == "auth0":
        # Auth0 claims might vary based on scopes requested. This is a common set.
        return UserProfile(
            provider="auth0",
            sub=raw_claims.get("sub", ""),
            email=raw_claims.get("email"),
            email_verified=raw_claims.get("email_verified"),
            name=raw_claims.get("name"),
            given_name=raw_claims.get("given_name"),
            family_name=raw_claims.get("family_name"),
            picture=raw_claims.get("picture"),
            locale=raw_claims.get("locale"),
        )
    else:
        # Default normalization or raise an error for unknown providers
        return UserProfile(
            provider=provider,
            sub=raw_claims.get("sub", ""),
            email=raw_claims.get("email"),
            name=raw_claims.get("name"),
        )


# Example usage
if __name__ == "__main__":
    google_raw_claims = {
        "sub": "1234567890",
        "email": "user@example.com",
        "email_verified": True,
        "name": "Test User",
        "given_name": "Test",
        "family_name": "User",
        "picture": "http://example.com/pic.jpg",
        "locale": "en",
    }
    normalized_google = normalize_claims("google", google_raw_claims)
    print("Normalized Google Claims:", normalized_google)

    auth0_raw_claims = {
        "sub": "auth0|abcdefg",
        "email": "auth0_user@example.com",
        "name": "Auth0 Test User",
    }
    normalized_auth0 = normalize_claims("auth0", auth0_raw_claims)
    print("Normalized Auth0 Claims:", normalized_auth0)

    token_data = {
        "access_token": "an_access_token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": "an_id_token",
        "refresh_token": "a_refresh_token",
        "scope": "openid profile email",
    }
    token_response = TokenResponse(**token_data)
    print("Token Response:", token_response)
