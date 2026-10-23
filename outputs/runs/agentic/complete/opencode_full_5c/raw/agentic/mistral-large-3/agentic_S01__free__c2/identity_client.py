from typing import Dict, Any
import os
import requests


class IdentityClient:
    def __init__(self):
        self.api_key = os.getenv("AUTH0_MANAGEMENT_API_KEY")
        self.domain = os.getenv("AUTH0_DOMAIN", "https://YOUR_TENANT.auth0.com")
        self.connection = os.getenv(
            "AUTH0_DB_CONNECTION", "Username-Password-Authentication"
        )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.domain}/api/v2/{endpoint}", json=payload, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def patch(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.patch(
            f"{self.domain}/api/v2/{endpoint}", json=payload, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.domain}/api/v2/{endpoint}", headers=self.headers
        )
        response.raise_for_status()
        return response.json()
