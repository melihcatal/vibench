import requests
import os
from typing import Dict, Any

# Auth0 Management API Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_MANAGEMENT_API_URL = f"https://{AUTH0_DOMAIN}/api/v2"
AUTH0_MANAGEMENT_AUDIENCE = f"https://{AUTH0_DOMAIN}/api/v2/"


def fetch_user_profile(access_token: str) -> Dict[str, Any]:
    """Fetch user profile from Auth0 Management API."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(f"{AUTH0_MANAGEMENT_API_URL}/userinfo", headers=headers)
    response.raise_for_status()
    return response.json()


def normalize_claims(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Auth0 profile claims into a standardized format."""
    normalized = {
        "sub": profile.get("sub"),
        "name": profile.get("name"),
        "given_name": profile.get("given_name"),
        "family_name": profile.get("family_name"),
        "email": profile.get("email"),
        "email_verified": profile.get("email_verified", False),
        "picture": profile.get("picture"),
        "locale": profile.get("locale"),
        "updated_at": profile.get("updated_at"),
        "nickname": profile.get("nickname"),
        "custom_claims": {k: v for k, v in profile.items() if k not in normalized},
    }
    return normalized
