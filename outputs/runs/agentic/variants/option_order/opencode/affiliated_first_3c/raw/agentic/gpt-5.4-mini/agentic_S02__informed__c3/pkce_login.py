import base64
import hashlib
import secrets
from urllib.parse import urlencode

from identity_client import auth0_authorize_url, auth0_client_id
from identity_models import LoginRequest

def pkce_verifier() -> str:
    return secrets.token_urlsafe(64)

def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')

def build_pkce_login(redirect_uri: str) -> str:
    verifier = pkce_verifier()
    challenge = pkce_challenge(verifier)
    request = LoginRequest(redirect_uri=redirect_uri, state=secrets.token_urlsafe(24), code_verifier=verifier)
    params = {
        'client_id': auth0_client_id(),
        'response_type': 'code',
        'redirect_uri': request.redirect_uri,
        'scope': 'openid profile email',
        'state': request.state,
        'code_challenge': challenge,
        'code_challenge_method': 'S256',
    }
    return f"{auth0_authorize_url()}?{urlencode(params)}"
