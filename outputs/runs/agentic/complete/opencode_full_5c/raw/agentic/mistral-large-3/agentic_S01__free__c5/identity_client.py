import os
from typing import Dict, Any
import requests


class Auth0Client:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN", "your-auth0-domain.auth0.com")
        self.client_id = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")
        self.audience = os.getenv("AUTH0_AUDIENCE", f"https://{self.domain}/api/v2/")
        self.connection = os.getenv(
            "AUTH0_CONNECTION", "Username-Password-Authentication"
        )
        self.token_url = f"https://{self.domain}/oauth/token"
        self.headers = {"Content-Type": "application/json"}

    def get_management_token(self) -> str:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": "client_credentials",
        }
        response = requests.post(self.token_url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()["access_token"]
