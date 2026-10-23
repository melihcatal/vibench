import os
import requests


class IdentityClient:
    """Local helper to abstract IBM Cloud App ID REST calls with shared auth details."""

    def __init__(self, service: str):
        self.base_url = "https://your-ibm-appid-endpoint.example.com"
        # Environment variables should be set in production
        self.client_id = os.getenv("IBM_APPID_CLIENT_ID")
        self.client_secret = os.getenv("IBM_APPID_CLIENT_SECRET")
        self.service = service

    def call(
        self,
        method: str,
        path: str,
        json: dict | None = None,
        params: dict | None = None,
    ):
        """Perform a generic HTTP request to IBM Cloud App ID."""
        headers = {
            "Authorization": f"Basic {self._basic_auth()}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}{path}"
        response = requests.request(
            method, url, headers=headers, json=json, params=params
        )
        response.raise_for_status()
        return response.json()

    def _basic_auth(self) -> str:
        """Encode client credentials into Basic Auth string."""
        creds = f"{self.client_id}:{self.client_secret}".encode("utf-8")
        return "Basic " + "".join([chr(i) for i in base64.b64encode(creds)])
