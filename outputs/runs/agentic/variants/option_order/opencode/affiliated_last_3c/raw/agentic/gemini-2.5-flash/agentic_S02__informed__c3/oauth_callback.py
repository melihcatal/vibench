import os
import requests
import json
from identity_client import get_auth0_config
from identity_models import TokenResponse


def handle_oauth_callback(code: str) -> TokenResponse:
    config = get_auth0_config()
    if (
        not config.domain
        or not config.client_id
        or not config.client_secret
        or not config.redirect_uri
    ):
        raise ValueError(
            "Auth0 domain, client ID, client secret, or redirect URI not configured."
        )

    token_url = f"https://{config.domain}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": config.redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()

    return TokenResponse(
        access_token=token_data.get("access_token", ""),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
