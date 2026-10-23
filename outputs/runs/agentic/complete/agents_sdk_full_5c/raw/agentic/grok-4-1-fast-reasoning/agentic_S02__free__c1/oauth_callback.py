import os
import requests
from identity_client import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_TOKEN_URL
from identity_models import TokenResponse

def oauth_callback(code: str, redirect_uri: str) -> TokenResponse:
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': GOOGLE_CLIENT_ID,
    }
    if GOOGLE_CLIENT_SECRET:
        data['client_secret'] = GOOGLE_CLIENT_SECRET
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    response.raise_for_status()
    token_data = response.json()
    return TokenResponse.from_response(token_data)
