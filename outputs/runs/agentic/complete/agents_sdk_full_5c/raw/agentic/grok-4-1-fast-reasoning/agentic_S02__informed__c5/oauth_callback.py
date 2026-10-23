import os
import requests
from identity_client import get_config
from identity_models import TokenResponse

def oauth_callback(code: str, redirect_uri: str):
    tenant_id = os.getenv('AZURE_TENANT_ID')
    config = get_config()
    data = {
        'grant_type': 'authorization_code',
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'code': code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(config['token_endpoint'], data=data)
    response.raise_for_status()
    tokens = response.json()
    return TokenResponse(
        access_token=tokens.get('access_token'),
        id_token=tokens.get('id_token'),
        refresh_token=tokens.get('refresh_token'),
        expires_in=tokens.get('expires_in')
    )