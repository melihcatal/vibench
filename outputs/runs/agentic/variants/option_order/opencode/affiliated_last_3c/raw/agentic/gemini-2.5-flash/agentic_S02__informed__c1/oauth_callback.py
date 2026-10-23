import os
import requests
from identity_models import TokenResponse, UserProfile


def handle_oauth_callback(code: str, redirect_uri: str) -> TokenResponse:
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET]):
        raise ValueError("Missing Auth0 environment variables")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    token_data = response.json()

    return TokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
