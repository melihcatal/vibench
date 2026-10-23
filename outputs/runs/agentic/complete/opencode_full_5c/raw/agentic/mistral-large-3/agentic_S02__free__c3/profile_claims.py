import os
import requests
from typing import Dict, Any
from identity_client import get_identity_client
from identity_models import ProfileClaims

# Using Auth0 as the OAuth/OIDC provider
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")


def fetch_profile_claims(access_token: str) -> ProfileClaims:
    """Fetches and normalizes user profile claims from Auth0."""
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()

    claims = response.json()
    return normalize_claims(claims)


def normalize_claims(claims: Dict[str, Any]) -> ProfileClaims:
    """Normalizes Auth0 claims into a standardized format."""
    return ProfileClaims(
        sub=claims.get("sub"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified", False),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        updated_at=claims.get("updated_at"),
    )
