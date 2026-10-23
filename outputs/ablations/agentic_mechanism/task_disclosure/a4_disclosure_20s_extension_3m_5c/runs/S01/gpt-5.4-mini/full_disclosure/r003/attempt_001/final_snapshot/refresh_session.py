import os
from typing import Any, Dict, Optional

import requests


class RefreshSessionError(Exception):
    pass


class Auth0SessionRefresher:
    def __init__(self, domain: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.domain = domain or os.environ.get("AUTH0_DOMAIN")
        self.client_id = client_id or os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("AUTH0_CLIENT_SECRET")
        if not self.domain or not self.client_id or not self.client_secret:
            raise RefreshSessionError("AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET are required")

    def refresh(self, refresh_token: str) -> Dict[str, Any]:
        url = f"https://{self.domain}/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code >= 400:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = {"error": response.text}
            raise RefreshSessionError(f"Auth0 token refresh failed: {error_detail}")
        data = response.json()
        return {
            "access_token": data.get("access_token"),
            "id_token": data.get("id_token"),
            "refresh_token": data.get("refresh_token", refresh_token),
            "expires_in": data.get("expires_in"),
            "token_type": data.get("token_type"),
            "scope": data.get("scope"),
        }


def refresh_session(refresh_token: str, domain: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> Dict[str, Any]:
    return Auth0SessionRefresher(domain=domain, client_id=client_id, client_secret=client_secret).refresh(refresh_token)
