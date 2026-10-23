import os
import requests

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_CALLBACK_URL,
    get_auth0_token_url,
)
from identity_models import OAuthTokens


def handle_oauth_callback(code: str, redirect_uri: str) -> OAuthTokens:
    """Handles the OAuth callback and exchanges an authorization code for tokens using Auth0.

    Args:
        code: The authorization code received from the identity provider.
        redirect_uri: The original redirect URI used in the authorization request.

    Returns:
        An OAuthTokens object containing the access token, ID token, and other token details.

    Raises:
        Exception: If token exchange fails.
    """
    token_url = get_auth0_token_url()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()

    return OAuthTokens(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        token_type=token_data.get("token_type"),
        expires_in=token_data.get("expires_in"),
    )
