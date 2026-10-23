import os
import webbrowser
from urllib.parse import urlencode
import requests
from identity_client import get_config, generate_pkce_pair
from identity_models import TokenResponse

def start_pkce_login(redirect_uri: str = 'http://localhost:8080/pkce-callback'):
    tenant_id = os.getenv('AZURE_TENANT_ID')
    config = get_config()
    verifier, challenge = generate_pkce_pair()
    params = {
        'client_id': config['client_id'],
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': config['scopes'],
        'code_challenge': challenge,
        'code_challenge_method': 'S256',
        'state': 'randomstate456',
    }
    auth_url = f"{config['authority']}/authorize?{urlencode(params)}"
    print(f"Visit this URL (save verifier: {verifier}): {auth_url}")
    webbrowser.open(auth_url)
    return verifier

def pkce_callback(verifier: str, code: str, redirect_uri: str) -> TokenResponse:
    tenant_id = os.getenv('AZURE_TENANT_ID')
    config = get_config()
    data = {
        'grant_type': 'authorization_code',
        'client_id': config['client_id'],
        'code': code,
        'redirect_uri': redirect_uri,
        'code_verifier': verifier,
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