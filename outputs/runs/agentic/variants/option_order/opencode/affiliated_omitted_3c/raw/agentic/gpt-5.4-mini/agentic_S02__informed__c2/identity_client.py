import base64
import hashlib
import os
from dataclasses import asdict
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import IdentityRequest, TokenResponse

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'example.auth0.com')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID', 'auth0-client-id')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET', '')
AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE', '')
AUTH0_SCOPE = os.environ.get('AUTH0_SCOPE', 'openid profile email offline_access')


def issuer_base_url() -> str:
    return f'https://{AUTH0_DOMAIN}'


def authorize_url(request: IdentityRequest) -> str:
    params: Dict[str, Any] = {
        'response_type': 'code',
        'client_id': AUTH0_CLIENT_ID,
        'redirect_uri': request.redirect_uri,
        'scope': AUTH0_SCOPE,
        'state': request.state,
    }
    if request.nonce:
        params['nonce'] = request.nonce
    if AUTH0_AUDIENCE:
        params['audience'] = AUTH0_AUDIENCE
    if request.code_verifier:
        challenge = base64.urlsafe_b64encode(hashlib.sha256(request.code_verifier.encode()).digest()).rstrip(b'=').decode()
        params['code_challenge'] = challenge
        params['code_challenge_method'] = 'S256'
    return f"{issuer_base_url()}/authorize?{urlencode(params)}"


def exchange_code(code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> TokenResponse:
    payload: Dict[str, Any] = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    if AUTH0_CLIENT_SECRET:
        payload['client_secret'] = AUTH0_CLIENT_SECRET
    if code_verifier:
        payload['code_verifier'] = code_verifier
    response = requests.post(f'{issuer_base_url()}/oauth/token', json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    return TokenResponse(
        access_token=data['access_token'],
        id_token=data.get('id_token'),
        refresh_token=data.get('refresh_token'),
        token_type=data.get('token_type'),
        expires_in=data.get('expires_in'),
    )


def userinfo(access_token: str) -> Dict[str, Any]:
    response = requests.get(f'{issuer_base_url()}/userinfo', headers={'Authorization': f'Bearer {access_token}'}, timeout=20)
    response.raise_for_status()
    return response.json()
