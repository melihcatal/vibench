import requests
import os
from urllib.parse import urlencode
from identity_client import get_cognito_config
from identity_models import OAuthTokenResponse

def handle_oauth_callback(code: str, redirect_uri: str, state: str, session_id: str) -> OAuthTokenResponse:
    if state != session_id: # Basic state check, in a real app this would be more robust
        raise ValueError("State mismatch")

    config = get_cognito_config()
    token_endpoint = config.token_endpoint
    client_id = config.client_id
    client_secret = config.client_secret

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    if client_secret:
        data["client_secret"] = client_secret

    try:
        response = requests.post(token_endpoint, headers=headers, data=urlencode(data))
        response.raise_for_status()
        token_data = response.json()
        return OAuthTokenResponse(
            access_token=token_data.get("access_token"),
            id_token=token_data.get("id_token"),
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type"),
            expires_in=token_data.get("expires_in")
        )
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Failed to exchange code for tokens: {e}. Response: {e.response.text}")
    except Exception as e:
        raise RuntimeError(f"An error occurred during token exchange: {e}")
