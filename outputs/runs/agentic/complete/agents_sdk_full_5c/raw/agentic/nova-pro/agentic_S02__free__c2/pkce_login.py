import requests
import hashlib
import base64
from identity_client import get_auth0_client

def pkce_login():
    client = get_auth0_client()
    code_verifier = base64.urlsafe_b64encode(hashlib.sha256(b'some-string').digest()).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')
    auth_url = f'https://{client.domain}/authorize'
    params = {
        'response_type': 'code',
        'client_id': client.client_id,
        'redirect_uri': 'https://yourapp.com/callback',
        'scope': 'openid profile email',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    response = requests.get(auth_url, params=params)
    return response.url, code_verifier