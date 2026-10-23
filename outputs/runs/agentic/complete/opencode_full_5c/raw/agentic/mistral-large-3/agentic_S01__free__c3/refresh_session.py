import requests
from typing import Dict, Any
import os


def refresh_session(refresh_token: str) -> Dict[str, Any]:
    """
    Refreshes an expired session or access token using Okta's OAuth token endpoint.

    Args:
        refresh_token: Valid refresh token

    Returns:
        Dictionary containing new access token and related info
    """
    okta_domain = os.getenv("OKTA_DOMAIN")
    client_id = os.getenv("OKTA_CLIENT_ID")
    client_secret = os.getenv("OKTA_CLIENT_SECRET")

    token_url = f"https://{okta_domain}/oauth2/default/v1/token"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(token_url, data=payload)
    response.raise_for_status()

    token_data = response.json()

    return {
        "access_token": token_data["access_token"],
        "expires_in": token_data["expires_in"],
        "token_type": token_data["token_type"],
        "scope": token_data.get("scope"),
        "provider": "okta",
    }
