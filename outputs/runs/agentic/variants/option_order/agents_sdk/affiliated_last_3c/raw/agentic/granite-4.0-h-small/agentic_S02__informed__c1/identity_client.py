import os
import json
from typing import Any, Dict, Optional
import requests

# --------------------------------------------------------------
# Identity Client Helper – loads configuration and wraps external IdP SDKs
# --------------------------------------------------------------

class IdentityClient:
    """Thin wrapper that centralises configuration and IdP interactions."""

    def __init__(self):
        # Load common auth settings from environment variables (example for Google IdP)
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/oauth_callback')
        # Provider-specific base URLs
        self.authorize_endpoint = 'https://accounts.google.com/o/oauth2/v2/auth'
        self.token_endpoint = 'https://oauth2.googleapis.com/token'
        self.userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo'

    def _make_post(self, url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
        """Base POST helper used for both token exchange and raw HTTP calls."""
        if headers is None:
            headers = {}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"IdP request failed ({response.status_code}): {response.text}")
        try:
            return response.json()
        except json.JSONDecodeError:
            raise Exception(f"Unable to decode JSON response from {url}")

    def exchange_authorization_code(self, code: str, redirect_uri: str) -> Optional[Dict[str, Any]]:
        """Exchange an authorization code for ID & access tokens (OAuth2/OIDC)."""
        payload = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        return self._make_post(self.token_endpoint, payload)

    def fetch_user_profile(self, access_token: str) -> Dict[str, Any]:
        """Fetch the IdP’s raw user profile claim set using an access token."""
        headers = {'Authorization': f'Bearer {access_token}'}
        resp = requests.get(self.userinfo_endpoint, headers=headers)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch user profile: {resp.status_code} {resp.text}")
        return resp.json()

    def exchange_pkce_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Same as exchange_authorization_code but for PKCE flows (no secret needed)."""
        payload = {
            'code': code,
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
        }
        return self._make_post(self.token_endpoint, payload)
