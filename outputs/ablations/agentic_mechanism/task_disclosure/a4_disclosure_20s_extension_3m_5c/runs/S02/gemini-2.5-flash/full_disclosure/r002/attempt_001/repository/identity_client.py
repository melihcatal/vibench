
import os
import requests
from typing import Dict, Any

class IdentityClientConfig:
    """
    Configuration for the Federated Login Flow client.
    Fetches values from environment variables.
    """
    def __init__(self):
        self.client_id = os.environ.get("OAUTH_CLIENT_ID")
        self.client_secret = os.environ.get("OAUTH_CLIENT_SECRET")
        self.authorization_url = os.environ.get("OAUTH_AUTHORIZATION_URL")
        self.token_url = os.environ.get("OAUTH_TOKEN_URL")
        self.redirect_uri = os.environ.get("OAUTH_REDIRECT_URI")
        self.userinfo_url = os.environ.get("OAUTH_USERINFO_URL")
        self.scope = os.environ.get("OAUTH_SCOPE", "openid profile email")

        if not all([self.client_id, self.authorization_url, self.token_url, self.redirect_uri]):
            raise ValueError("Missing one or more required OAuth configuration environment variables (OAUTH_CLIENT_ID, OAUTH_AUTHORIZATION_URL, OAUTH_TOKEN_URL, OAUTH_REDIRECT_URI)")

class IdentityClient:
    """
    Helper utilities for making HTTP requests in the Federated Login Flow.
    """
    def __init__(self, config: IdentityClientConfig):
        self.config = config

    def post_token_request(self, data: Dict[str, str]) -> requests.Response:
        """
        Makes a POST request to the token endpoint.
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.config.token_url, data=data, headers=headers)
        response.raise_for_status()
        return response

    def get_userinfo(self, access_token: str) -> Dict[str, Any]:
        """
        Makes a GET request to the userinfo endpoint.
        """
        if not self.config.userinfo_url:
            raise ValueError("OAUTH_USERINFO_URL is not configured.")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.config.userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()

