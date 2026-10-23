import os
import requests
from typing import Dict, Any
from urllib.parse import urljoin


class Auth0ManagementClient:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.audience = os.environ.get("AUTH0_MANAGEMENT_AUDIENCE")
        self.token = self._get_management_api_token()

        if not all(
            [self.domain, self.client_id, self.client_secret, self.audience, self.token]
        ):
            raise ValueError(
                "Missing one or more Auth0 environment variables (AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_MANAGEMENT_AUDIENCE)."
            )

    def _get_management_api_token(self) -> str:
        token_url = f"https://{self.domain}/oauth/token"
        headers = {"content-type": "application/json"}
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": "client_credentials",
        }
        response = requests.post(token_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def post(self, path: str, data: Dict[str, Any]) -> requests.Response:
        url = urljoin(self.audience + "/", path.lstrip("/"))
        return requests.post(url, headers=self._get_headers(), json=data)

    def patch(self, path: str, data: Dict[str, Any]) -> requests.Response:
        url = urljoin(self.audience + "/", path.lstrip("/"))
        return requests.patch(url, headers=self._get_headers(), json=data)


class Auth0AuthenticationClient:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")

        if not all([self.domain, self.client_id]):
            raise ValueError(
                "Missing one or more Auth0 environment variables (AUTH0_DOMAIN, AUTH0_CLIENT_ID)."
            )

    def post(self, path: str, data: Dict[str, Any]) -> requests.Response:
        url = f"https://{self.domain}/{path.lstrip('/')}"
        headers = {"content-type": "application/json"}
        return requests.post(url, headers=headers, json=data)
