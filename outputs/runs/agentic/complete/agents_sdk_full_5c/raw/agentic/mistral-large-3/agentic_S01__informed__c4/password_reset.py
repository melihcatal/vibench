import os
import requests
from typing import Dict, Any

class PasswordResetInitiator:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.token_url = f"https://{self.domain}/oauth/token"
        self.db_connections_url = f"https://{self.domain}/api/v2/dbconnections/"

    def _get_management_token(self) -> str:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": f"https://{self.domain}/api/v2/",
            "grant_type": "client_credentials"
        }
        response = requests.post(self.token_url, json=payload)
        response.raise_for_status()
        return response.json()["access_token"]

    def initiate_password_reset(self, email: str, connection: str = "Username-Password-Authentication") -> Dict[str, Any]:
        token = self._get_management_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": email,
            "connection": connection
        }
        response = requests.post(f"https://{self.domain}/dbconnections/change_password", json=payload, headers=headers)
        response.raise_for_status()
        return {"status": "password_reset_email_sent"}