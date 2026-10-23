"""
refresh_session.py
Refreshes an expired session or access token via Auth0 Authentication API.

Provider: Auth0 (requests / REST)
Auth: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
"""

import os
import requests
from identity_client import get_auth0_domain, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(request: RefreshRequest) -> RefreshResponse:
    """
    Refreshes an expired Auth0 access token using a valid refresh token.

    Args:
        request: RefreshRequest containing the current refresh token.

    Returns:
        RefreshResponse with new access token, id token, refresh token, and expiry.
    """
    domain = get_auth0_domain()
    token_url = f"https://{domain}/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "refresh_token": request.refresh_token,
    }

    response = requests.post(token_url, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()

    return RefreshResponse(
        access_token=data.get("access_token"),
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token", request.refresh_token),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 86400),
        scope=data.get("scope"),
    )


if __name__ == "__main__":
    req = RefreshRequest(refresh_token="existing_refresh_token_here")
    resp = refresh_session(req)
    print(f"Refreshed session. New token expires in {resp.expires_in}s")
