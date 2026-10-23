import os
import requests
from identity_client import Auth0Client
from identity_models import RefreshSessionRequest, RefreshSessionResponse


class SessionRefresher:
    def __init__(self):
        self.client = Auth0Client()

    def refresh_session(self, request: RefreshSessionRequest) -> RefreshSessionResponse:
        url = f"https://{self.client.domain}/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client.client_id,
            "client_secret": self.client.client_secret,
            "refresh_token": request["refresh_token"],
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return self.client._normalize_refresh_response(response.json())