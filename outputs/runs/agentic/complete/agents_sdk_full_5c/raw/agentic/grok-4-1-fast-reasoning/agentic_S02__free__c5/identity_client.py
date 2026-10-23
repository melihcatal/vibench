import os
import secrets
import hashlib
import base64
import urllib.parse
from typing import Optional, Tuple

class Auth0Client:
    def __init__(self):
        self.domain = os.getenv('AUTH0_DOMAIN')  # e.g., 'dev-xxx.us.auth0.com'
        self.client_id = os.getenv('AUTH0_CLIENT_ID')
        self.client_secret = os.getenv('AUTH0_CLIENT_SECRET')  # optional for PKCE
        self.redirect_uri = os.getenv('AUTH0_REDIRECT_URI', 'http://localhost:3000/callback')

    @staticmethod
    def generate_pkce_pair() -> Tuple[str, str]:
        verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('ascii')
        digester = hashlib.sha256(verifier.encode('ascii')).digest()
        challenge = base64.urlsafe_b64encode(digester).rstrip(b'=').decode('ascii')
        return verifier, challenge

    def get_authorize_url(self, scope: str = 'openid profile email', state: Optional[str] = None,
                          code_challenge: Optional[str] = None) -> str:
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': scope,
        }
        if state:
            params['state'] = state
        if code_challenge:
            params['code_challenge'] = code_challenge
            params['code_challenge_method'] = 'S256'
        return f"https://{self.domain}/authorize?{urllib.parse.urlencode(params)}"