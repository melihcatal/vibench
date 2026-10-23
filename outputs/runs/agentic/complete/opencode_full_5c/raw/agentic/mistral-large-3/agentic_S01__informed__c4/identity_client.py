import os
from typing import Dict, Any
import requests
from identity_models import (
    RegisterRequest,
    RegisterResponse,
    normalize_register_request,
    normalize_register_response,
)


class IdentityClient:
    def __init__(self):
        self.auth0_domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.token_url = f"https://{self.auth0_domain}/oauth/token"
        self.api_base_url = f"https://{self.auth0_domain}/api/v2"
        self._access_token = None

    def _get_access_token(self) -> str:
        if not self._access_token:
            payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "audience": f"https://{self.auth0_domain}/api/v2/",
                "grant_type": "client_credentials",
            }
            response = requests.post(self.token_url, json=payload)
            response.raise_for_status()
            self._access_token = response.json().get("access_token")
        return self._access_token

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json",
        }

    def register_user(self, request: RegisterRequest) -> RegisterResponse:
        normalized_request = normalize_register_request(request)
        url = f"{self.api_base_url}/users"
        response = requests.post(url, headers=self._headers(), json=normalized_request)
        response.raise_for_status()
        return normalize_register_response(response.json())
