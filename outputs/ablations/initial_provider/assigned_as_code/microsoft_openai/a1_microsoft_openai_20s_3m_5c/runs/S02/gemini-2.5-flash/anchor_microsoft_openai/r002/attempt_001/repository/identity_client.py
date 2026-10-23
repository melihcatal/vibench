import os
import base64
import hashlib
import secrets
import msal
from urllib.parse import urlencode

class IdentityClient:
    def __init__(self, client_id: str, client_secret: str, tenant_id: str, authority_url: str = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.authority_url = authority_url or f"https://login.microsoftonline.com/{tenant_id}"
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority_url,
            client_credential=self.client_secret,
        )

    @staticmethod
    def generate_pkce_challenge():
        code_verifier = secrets.token_urlsafe(96)  # Generate a high-entropy cryptographically random string
        s256 = hashlib.sha256()
        s256.update(code_verifier.encode('utf-8'))
        code_challenge = base64.urlsafe_b64encode(s256.digest()).decode('utf-8').replace('=', '')
        return code_verifier, code_challenge

    def get_authorization_url(self, scopes: list, redirect_uri: str, state: str = None, code_challenge: str = None, code_challenge_method: str = 'S256'):
        params = {
            'scope': ' '.join(scopes),
            'redirect_uri': redirect_uri,
            'client_id': self.client_id,
            'response_type': 'code',
            'response_mode': 'query',
        }
        if state:
            params['state'] = state
        if code_challenge:
            params['code_challenge'] = code_challenge
            params['code_challenge_method'] = code_challenge_method

        return f"{self.authority_url}/oauth2/v2.0/authorize?{urlencode(params)}"

    def acquire_token_by_auth_code(self, authorization_code: str, redirect_uri: str, scopes: list, code_verifier: str = None):
        return self.app.acquire_token_by_authorization_code(
            authorization_code,
            scopes=scopes,
            redirect_uri=redirect_uri,
            pkce_code_verifier=code_verifier
        )

    def acquire_token_silent(self, scopes: list, account):
        return self.app.acquire_token_silent(scopes, account)

    def get_accounts(self):
        return self.app.get_accounts()
