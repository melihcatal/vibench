import os
import requests
from identity_client import IdentityClient

def refresh_session(refresh_token: str):
    """Refresh an expired Auth0 session using a refresh token.

    Returns new tokens (access_token, id_token, refresh_token) on success.
    Raises for invalid token or server error.
    """
    client = IdentityClient()
    payload = {
        "grant_type": "refresh_token",
        "client_id": client.auth0_client_id,
        "client_secret": client.auth0_client_secret,
        "refresh_token": refresh_token,
        "audience": client.auth0_api_audience,
    }
    response = requests.post(
        f"{client.auth0_domain}/oauth/token",
        data=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
