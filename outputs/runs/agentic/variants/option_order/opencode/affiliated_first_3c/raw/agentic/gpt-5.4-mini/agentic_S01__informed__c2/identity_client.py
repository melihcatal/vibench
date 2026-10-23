import os
from typing import Dict

import requests

from identity_models import normalize_email


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")


class Auth0Client:
    def __init__(
        self,
        domain: str = AUTH0_DOMAIN,
        client_id: str = AUTH0_CLIENT_ID,
        client_secret: str = AUTH0_CLIENT_SECRET,
        audience: str = AUTH0_AUDIENCE,
    ):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience
        self.base_url = f"https://{domain}"

    def headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def token_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.get_management_token()}",
            "Content-Type": "application/json",
        }

    def get_management_token(self) -> str:
        response = requests.post(
            f"https://{self.domain}/oauth/token",
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "audience": self.audience or f"https://{self.domain}/api/v2/",
                "grant_type": "client_credentials",
            },
            headers=self.headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def normalize(self, email: str) -> str:
        return normalize_email(email)
