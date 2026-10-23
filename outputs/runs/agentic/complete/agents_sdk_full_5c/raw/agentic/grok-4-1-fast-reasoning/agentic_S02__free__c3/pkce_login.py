import secrets
import base64
import hashlib
import urllib.parse
import requests
from .identity_client import GOOGLE_CONFIG
from .identity_models import OAuthConfig, TokenResponse

def generate_pkce_pair() -&gt; tuple[str, str]:
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('ascii').rstrip('=')
    code_challenge_hash = hashlib.sha256(code_verifier.encode('ascii')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge_hash).decode('ascii').rstrip('=')
    return code_verifier, code_challenge

def start_pkce_login() -&gt; tuple[str, str]:
    config: OAuthConfig = GOOGLE_CONFIG
    verifier, challenge = generate_pkce_pair()
    params = {
        'client_id': config.client_id,
        'redirect_uri': config.redirect_uri,
        'scope': ' '.join(config.scopes),
        'response_type': 'code',
        'code_challenge': challenge,
        'code_challenge_method': 'S256',
    }
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{config.auth_url}?{query_string}"
    return auth_url, verifier

def exchange_pkce_code(code: str, verifier: str) -&gt; TokenResponse:
    config: OAuthConfig = GOOGLE_CONFIG
    data = {
        'client_id': config.client_id,
        'code': code,
        'code_verifier': verifier,
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
