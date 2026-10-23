import os
import requests
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> RefreshResponse:
    """Refresh an expired session or access token using Auth0."""
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")

    if not all([domain, client_id, client_secret]):
        raise ValueError("Missing Auth0 environment variables")

    url = f"https://{domain}/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    headers = {"content-type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return RefreshResponse(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", refresh_token),
            id_token=data.get("id_token"),
            expires_in=data["expires_in"],
            token_type=data["token_type"],
            provider="auth0",
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Auth0 token refresh failed: {str(e)}")
