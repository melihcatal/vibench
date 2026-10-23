import requests

from identity_client import auth0_client_id, auth0_client_secret, auth0_token_url
from identity_models import TokenResponse

def exchange_code(code: str, redirect_uri: str) -> TokenResponse:
    data = {
        'grant_type': 'authorization_code',
        'client_id': auth0_client_id(),
        'client_secret': auth0_client_secret(),
        'code': code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(auth0_token_url(), data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return TokenResponse(
        access_token=payload['access_token'],
        id_token=payload.get('id_token'),
        refresh_token=payload.get('refresh_token'),
        expires_in=payload.get('expires_in'),
        token_type=payload.get('token_type'),
        raw=payload,
    )
