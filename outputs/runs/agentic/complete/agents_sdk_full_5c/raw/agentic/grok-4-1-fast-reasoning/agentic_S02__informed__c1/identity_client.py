import secrets
import hashlib
import base64
import urllib.parse
import requests
from typing import Optional, Tuple
from identity_models import TokenResponse

def generate_pkce_verifier_and_challenge() -> Tuple[str, str]:
    verifier_bytes = secrets.token_bytes(32)
    verifier = base64.urlsafe_b64encode(verifier_bytes).decode('utf-8').rstrip('=')
    challenge_bytes = hashlib.sha256(verifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(challenge_bytes).decode('utf-8').rstrip('=')
    return verifier, challenge

def build_authorize_url(authorize_endpoint: str, client_id: str, redirect_uri: str,
                        scope: str = 'openid profile email', state: Optional[str] = None,
                        code_challenge: Optional[str] = None,
                        code_challenge_method: str = 'S256') -> str:
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
    }
    if state:
        params['state'] = state
    if code_challenge:
        params['code_challenge'] = code_challenge
        params['code_challenge_method'] = code_challenge_method
    return authorize_endpoint + '?' + urllib.parse.urlencode(params)

def exchange_authorization_code(token_endpoint: str, client_id: str, code: str, redirect_uri: str,
                                client_secret: Optional[str] = None,
                                code_verifier: Optional[str] = None) -> TokenResponse:
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    if client_secret is not None:
        data['client_secret'] = client_secret
    if code_verifier is not None:
        data['code_verifier'] = code_verifier
    response = requests.post(token_endpoint, data=data)
    response.raise_for_status()
    return TokenResponse(**response.json())
