import os
from typing import Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import OAuthTokenResponse


class Auth0IdentityClient:
    def __init__(self, domain: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.domain = domain or os.environ.get('AUTH0_DOMAIN', '')
        self.client_id = client_id or os.environ.get('AUTH0_CLIENT_ID', '')
        self.client_secret = client_secret or os.environ.get('AUTH0_CLIENT_SECRET', '')
        self.audience = os.environ.get('AUTH0_AUDIENCE')
        self.issuer = f'https://{self.domain}' if self.domain else ''

    def authorization_url(self, redirect_uri: str, state: str, scope: str = 'openid profile email', code_challenge: Optional[str] = None) -> str:
        params = {'response_type': 'code', 'client_id': self.client_id, 'redirect_uri': redirect_uri, 'scope': scope, 'state': state}
        if self.audience:
            params['audience'] = self.audience
        if code_challenge:
            params['code_challenge'] = code_challenge
            params['code_challenge_method'] = 'S256'
        return f'{self.issuer}/authorize?{urlencode(params)}'

    def token_endpoint(self) -> str:
        return f'{self.issuer}/oauth/token'

    def userinfo_endpoint(self) -> str:
        return f'{self.issuer}/userinfo'

    def exchange_code(self, code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> OAuthTokenResponse:
        payload: Dict[str, str] = {'grant_type': 'authorization_code', 'client_id': self.client_id, 'client_secret': self.client_secret, 'code': code, 'redirect_uri': redirect_uri}
        if code_verifier:
            payload['code_verifier'] = code_verifier
        resp = requests.post(self.token_endpoint(), json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        return OAuthTokenResponse(access_token=data['access_token'], id_token=data.get('id_token'), refresh_token=data.get('refresh_token'), token_type=data.get('token_type'), expires_in=data.get('expires_in'))

    def fetch_profile(self, access_token: str) -> Dict[str, object]:
        resp = requests.get(self.userinfo_endpoint(), headers={'Authorization': f'Bearer {access_token}'}, timeout=20)
        resp.raise_for_status()
        return resp.json()
