import os
import requests
from identity_client import TOKEN_ENDPOINT, get_google_client_config
from identity_models import AuthTokenResponse

def handle_google_oauth_callback(code: str) -> AuthTokenResponse:
    client_id, client_secret, redirect_uri = get_google_client_config()

    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(TOKEN_ENDPOINT, data=token_data)
    response.raise_for_status()
    
    return AuthTokenResponse(response.json())
