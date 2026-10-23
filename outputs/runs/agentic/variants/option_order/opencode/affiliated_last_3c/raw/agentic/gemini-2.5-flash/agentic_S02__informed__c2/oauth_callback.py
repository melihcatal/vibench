import os
import json
import requests

from identity_client import (
    get_auth0_domain,
    get_auth0_client_id,
    get_auth0_client_secret,
)
from identity_models import OAuthTokenResponse


def handle_oauth_callback(authorization_code: str) -> OAuthTokenResponse:
    """Handles the Auth0 callback and exchanges an authorization code for tokens."""
    auth0_domain = get_auth0_domain()
    auth0_client_id = get_auth0_client_id()
    auth0_client_secret = get_auth0_client_secret()
    redirect_uri = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )

    token_url = f"https://{auth0_domain}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": auth0_client_id,
        "client_secret": auth0_client_secret,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    token_data = response.json()
    return OAuthTokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
        scope=token_data.get("scope"),
    )
