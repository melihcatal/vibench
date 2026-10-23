import base64
import hashlib
import os
import secrets
from urllib.parse import urlencode

from identity_client import auth0_authorize_url, auth0_client_id, auth0_issuer
from identity_models import LoginRequest

def start_login(redirect_uri: str) -> str:
    state = secrets.token_urlsafe(24)
    nonce = secrets.token_urlsafe(24)
    request = LoginRequest(redirect_uri=redirect_uri, state=state, nonce=nonce)
    params = {
        'client_id': auth0_client_id(),
        'response_type': 'code',
        'redirect_uri': request.redirect_uri,
        'scope': 'openid profile email',
        'state': request.state,
        'nonce': request.nonce,
        'audience': os.getenv('AUTH0_AUDIENCE', 'https://api.example.com'),
        'issuer': auth0_issuer(),
    }
    return f"{auth0_authorize_url()}?{urlencode(params)}"

def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')
