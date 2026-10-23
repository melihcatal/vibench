import os
import requests
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> RefreshResponse:
    """Refresh an expired access token using Auth0 refresh token."""
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    # Auth0 OAuth token endpoint for refresh token grant
    token_url = f"https://{domain}/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()

    token_data = response.json()

    return RefreshResponse(
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token", refresh_token),
        id_token=token_data.get("id_token"),
        expires_in=token_data["expires_in"],
        token_type=token_data["token_type"],
    )
