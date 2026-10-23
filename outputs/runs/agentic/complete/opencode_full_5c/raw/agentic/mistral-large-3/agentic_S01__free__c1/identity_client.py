import os
from typing import Dict, Any
import requests


class Auth0IdentityClient:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN", "your-auth0-domain.auth0.com")
        self.client_id = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")
        self.audience = os.getenv("AUTH0_AUDIENCE", f"https://{self.domain}/api/v2/")
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

    def create_user(
        self,
        email: str,
        password: str,
        connection: str = "Username-Password-Authentication",
    ) -> Dict[str, Any]:
        url = f"https://{self.domain}/api/v2/users"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.get_management_token()}",
        }
        payload = {"email": email, "password": password, "connection": connection}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def login_user(
        self, email: str, password: str, realm: str = "Username-Password-Authentication"
    ) -> Dict[str, Any]:
        url = f"https://{self.domain}/oauth/token"
        payload = {
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": email,
            "password": password,
            "realm": realm,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        url = f"https://{self.domain}/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def start_password_reset(
        self, email: str, connection: str = "Username-Password-Authentication"
    ) -> None:
        url = f"https://{self.domain}/dbconnections/change_password"
        payload = {
            "client_id": self.client_id,
            "email": email,
            "connection": connection,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
