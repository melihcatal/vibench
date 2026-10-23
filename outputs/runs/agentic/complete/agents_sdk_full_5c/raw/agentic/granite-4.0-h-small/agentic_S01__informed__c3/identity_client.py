import os
import requests
from typing import Any, Dict, Optional
from identity_models import BaseResponse

class IdentityClient:
    """Thin wrapper around Auth0 Management API using raw HTTP requests."""
    def __init__(self, base_url: str, client_id: str, audience: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.audience = audience
        # Obtain the JWT for management API calls from environment variables
        self.access_token = os.getenv('AUTH0_MANAGEMENT_TOKEN')

    def _request(self, method: str, endpoint: str, json: Optional[Dict[str, Any]] = None,
                 params: Optional[Dict[str, Any]] = None, provider: str = 'auth0') -> Dict[str, Any]:
        url = f'{self.base_url}{endpoint}'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        auth0_headers = {
            # Provider identifier signal (required by task)
            'X-Provider': provider
        }
        headers.update(auth0_headers)
        response = requests.request(method, url, json=json, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def register_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request('POST', '/api/v2/users', json=payload)

    def exchange_password(self, payload: Dict[str, Any], provider: str) -> Dict[str, Any]:
        return self._request('POST', '/oauth/token', json=payload)

    def refresh_token(self, payload: Dict[str, Any], provider: str) -> Dict[str, Any]:
        return self._request('POST', '/oauth/token', json=payload)

    def start_password_reset(self, payload: Dict[str, Any], provider: str) -> Dict[str, Any]:
        return self._request('POST', '/api/v2/tickets/password-change', json=payload)

    def test_connection(self) -> bool:
        try:
            self._request('GET', '/api/v2/connections')
            return True
        except Exception:
            return False

# Helper to create payloads elsewhere
# Example usage:
# client = IdentityClient(base_url='https://mytenant.auth0.com', client_id='myclient',
#                         access_token=os.getenv('AUTH0_MANAGEMENT_TOKEN'))
