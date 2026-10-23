import os
import requests
from typing import Dict, Any


class Auth0Client:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.management_api_audience = f"https://{self.domain}/api/v2/"
        self.management_api_token = self._get_management_api_token()

    def _get_management_api_token(self) -> str:
        # This would typically be cached and refreshed
        url = f"https://{self.domain}/oauth/token"
        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.management_api_audience,
            "grant_type": "client_credentials",
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_management_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.management_api_token}",
            "Content-Type": "application/json",
        }

    def get_auth_headers(self, token: str = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def get_auth_url(self, path: str) -> str:
        return f"https://{self.domain}{path}"
