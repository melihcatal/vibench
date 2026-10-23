import os
import requests

class Auth0Client:
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.audience = f"https://{self.domain}/api/v2/" # Management API Audience
        self._management_api_token = None

        if not all([self.domain, self.client_id, self.client_secret]):
            raise ValueError("AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET environment variables must be set.")

    def _get_management_api_token(self):
        if self._management_api_token:
            return self._management_api_token

        token_url = f"https://{self.domain}/oauth/token"
        headers = {"Content-Type": "application/json"}
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": "client_credentials"
        }
        response = requests.post(token_url, headers=headers, json=payload)
        response.raise_for_status()
        self._management_api_token = response.json().get("access_token")
        return self._management_api_token

    def get_management_api_headers(self):
        return {
            "Authorization": f"Bearer {self._get_management_api_token()}",
            "Content-Type": "application/json"
        }

    def get_authentication_api_url(self, path: str):
        return f"https://{self.domain}{path}"

auth0_client = Auth0Client()
