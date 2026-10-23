
import os
import requests
from typing import Dict, Any

# Auth0 specific configuration
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"

def fetch_and_normalize_profile_claims(access_token: str) -> Dict[str, Any]:
    """
    Fetches user profile claims from Auth0 and normalizes them.

    Args:
        access_token: The access token obtained during the federated login flow.

    Returns:
        A dictionary containing normalized user profile claims.
    """
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN environment variable not set.")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(AUTH0_USERINFO_URL, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    userinfo = response.json()

    # Normalize claims
    normalized_claims = {
        "sub": userinfo.get("sub"),
        "name": userinfo.get("name"),
        "email": userinfo.get("email"),
        "picture": userinfo.get("picture"),
        "federated_provider": "Auth0", # Explicitly identify the provider
        # Add other claims as needed, mapping Auth0 specific claims to a generic format
    }
    return normalized_claims

