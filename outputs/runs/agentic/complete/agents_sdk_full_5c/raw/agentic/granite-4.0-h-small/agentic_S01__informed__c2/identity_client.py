import os
import requests
from typing import Any, Dict

# Configuration for Auth0 (environment variables)
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

BASE_URL = f'https://{AUTH0_DOMAIN}"

class IdentityClient:
    def __init__(self, auth0_domain: str, auth0_client_id: str, auth0_client_secret: str = None):
        self.auth0_domain = auth0_domain
        self.auth0_client_id = auth0_client_id
        self.auth0_client_secret = auth0_client_secret
        self.access_token = self._fetch_management_token()

    def _fetch_management_token(self) -> str:
        """Obtain a JWT for the Auth0 Management API."""
        token_url = f'https://{self.auth0_domain}/oauth/token'
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.auth0_client_id,
            'client_secret': self.auth0_client_secret,
            'audience': f'https://{self.auth0_domain}/api/v2/'
        }
        resp = requests.post(token_url, json=payload)
        resp.raise_for_status()
        return resp.json()['access_token']

    def _request(self, method: str, endpoint: str, json: Dict = None, params: Dict = None) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        url = f'https://{self.auth0_domain}{endpoint}'
        resp = requests.request(method, url, headers=headers, json=json, params=params)
        resp.raise_for_status()
        return resp.json()

    # Auth0 Management API wrappers
    def register_user(self, payload: Dict) -> Dict:
        """POST /api/v2/users"""
        return self._request('POST', '/api/v2/users', json=payload)

    def authenticate_with_password_grant(self, payload: Dict) -> Dict:
        """POST /oauth/token (password grant)"""
        return self._request('POST', '/oauth/token', json=payload)

    def refresh_access_token(self, payload: Dict) -> Dict:
        """POST /oauth/token (refresh token grant)"""
        return self._request('POST', '/oauth/token', json=payload)

    def request_password_reset(self, payload: Dict) -> bool:
        """POST /api/v2/tickets/password-recovery"""
        resp = self._request('POST', '/api/v2/tickets/password-recovery', json=payload)
        return resp.get('ticket_sent')
