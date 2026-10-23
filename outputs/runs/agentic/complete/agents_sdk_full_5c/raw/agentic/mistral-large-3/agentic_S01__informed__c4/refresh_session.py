import os
import requests
from typing import Dict, Any

class SessionRefresher:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.token_url = f"https://{self.domain}/oauth/token"

    def refresh_session(self, refresh_token: str) -> Dict[str, Any]:
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token
        }
        response = requests.post(self.token_url, json=payload)
        response.raise_for_status()
        return response.json()