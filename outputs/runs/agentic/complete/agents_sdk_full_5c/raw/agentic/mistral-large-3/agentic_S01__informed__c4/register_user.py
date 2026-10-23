import os
from typing import Dict, Any
import requests

class UserRegistrar:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.audience = f"https://{self.domain}/api/v2/"
        self.token_url = f"https://{self.domain}/oauth/token"
        self.users_url = f"https://{self.domain}/api/v2/users"

    def _get_management_token(self) -> str:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": "client_credentials"
        }
        response = requests.post(self.token_url, json=payload)
        response.raise_for_status()
        return response.json()["access_token"]

    def register_user(self, email: str, password: str, connection: str = "Username-Password-Authentication") -> Dict[str, Any]:
        token = self._get_management_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": email,
            "password": password,
            "connection": connection,
            "email_verified": False
        }
        response = requests.post(self.users_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()