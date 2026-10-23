import os
import requests
from identity_client import Auth0Client
from identity_models import LoginRequest, LoginResponse


class UserAuthenticator:
    def __init__(self):
        self.client = Auth0Client()

    def login(self, request: LoginRequest) -> LoginResponse:
        url = f"https://{self.client.domain}/oauth/token"
        payload = {
            "grant_type": "password",
            "username": request["email"],
            "password": request["password"],
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
            "audience": self.client.audience,
            "scope": "openid profile email offline_access",
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return self.client._normalize_login_response(response.json())