import os
import requests
from typing import Dict, Any

class EmailPasswordAuthenticator:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.token_url = f"https://{self.domain}/oauth/token"

    def login(self, email: str, password: str, realm: str = "Username-Password-Authentication") -> Dict[str, Any]:
        payload = {
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": email,
            "password": password,
            "realm": realm,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": f"https://{self.domain}/api/v2/"
        }
        response = requests.post(self.token_url, json=payload)
        response.raise_for_status()
        return response.json()