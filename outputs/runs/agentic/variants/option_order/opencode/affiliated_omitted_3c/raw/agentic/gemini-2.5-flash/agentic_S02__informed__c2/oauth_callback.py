import os
import json
import requests
from typing import Dict, Any
from identity_models import OAuthTokenResponse

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")


def handle_oauth_callback(authorization_code: str, state: str) -> OAuthTokenResponse:
    if (
        not AUTH0_DOMAIN
        or not AUTH0_CLIENT_ID
        or not AUTH0_CLIENT_SECRET
        or not AUTH0_CALLBACK_URL
    ):
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, and AUTH0_CALLBACK_URL must be set."
        )

    # In a real application, you would validate the 'state' parameter here
    # For demonstration, we'll skip validation.

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    token_data: Dict[str, Any] = response.json()
    return OAuthTokenResponse(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
