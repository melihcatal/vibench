import os
import requests
from typing import Dict, Any
from identity_client import Auth0Client
from identity_models import RegisterUserRequest, RegisterUserResponse


class UserRegistrar:
    def __init__(self):
        self.client = Auth0Client()

    def register_user(self, request: RegisterUserRequest) -> RegisterUserResponse:
        url = f"https://{self.client.domain}/dbconnections/signup"
        payload = {
            "client_id": self.client.client_id,
            "email": request["email"],
            "password": request["password"],
            "connection": self.client.connection,
            "given_name": request.get("given_name", ""),
            "family_name": request.get("family_name", ""),
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return self.client._normalize_register_response(response.json())