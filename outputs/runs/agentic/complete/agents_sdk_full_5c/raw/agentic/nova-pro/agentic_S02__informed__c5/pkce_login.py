import os
import requests
import uuid
from urllib.parse import urlencode

AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')

def pkce_login():
    code_verifier = uuid.uuid4().hex
    code_challenge = uuid.uuid4().hex
    authorization_endpoint = f'https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/authorize'
    params = {
        'response_type': 'code',
        'client_id': AZURE_CLIENT_ID,
        'redirect_uri': 'https://yourapp.com/callback',
        'scope': 'openid profile email',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    url = f'{authorization_endpoint}?{urlencode(params)}'
    return url, code_verifier