import os
import secrets
import hashlib
import base64

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
GOOGLE_SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
]

def generate_pkce_pair() -> tuple[str, str]:
    """Returns (code_verifier, code_challenge)"""
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('ascii').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('ascii')).digest()
    ).decode('ascii').rstrip('=')
    return code_verifier, code_challenge

def build_auth_params(
    client_id: str,
    redirect_uri: str,
    scopes: list[str],
    state: str | None = None,
    code_challenge: str | None = None,
    code_challenge_method: str = 'S256',
) -> dict:
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes),
        'response_type': 'code',
    }
    if state:
        params['state'] = state
    if code_challenge:
        params['code_challenge'] = code_challenge
        params['code_challenge_method'] = code_challenge_method
    return params
