import requests
import os
from .identity_client import GOOGLE_CONFIG
from .identity_models import TokenResponse

def handle_oauth_callback(code: str, state: str) -&gt; TokenResponse:
    config = GOOGLE_CONFIG
    data = {
        'client_id': config.client_id,
        'client_secret': config.client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': config.redirect_uri,
    }
    response = requests.post(config.token_url, data=data)
    response.raise_for_status()
    tokens = response.json()
    return TokenResponse(
        access_token=tokens['access_token'],
        id_token=tokens.get('id_token'),
        refresh_token=tokens.get('refresh_token'),
        token_type=tokens.get('token_type', 'Bearer'),
        expires_in=tokens.get('expires_in', 3600)
    )
