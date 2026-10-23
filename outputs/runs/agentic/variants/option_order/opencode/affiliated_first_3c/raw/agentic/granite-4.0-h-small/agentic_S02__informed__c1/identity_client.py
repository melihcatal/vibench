import os
import requests
from typing import Any, Dict


# Helper functions for loading env vars with defaults
def getenv_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name, str(default)).lower()
    return val in ("true", "1", "yes")


def getenv_int(name: str, default: int = 0) -> int:
    return int(os.getenv(name, default))


def getenv_str(name: str, default: str = "") -> str:
    return os.getenv(name, default)


class IdentityClient:
    """Local helper to encapsulate configuration and provider‑specific calls.

    This file demonstrates how the same‑scenario and later‑step files load
    provider‑specific credentials and instantiate a concrete client.
    """

    def __init__(
        self, base_url: str, client_id: str, client_secret: str = "", **kwargs
    ):
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        # Additional provider‑specific kwargs can be stored for later use
        self.extra = kwargs

    def generate_authorize_url(
        self, redirect_uri: str, scope: str, response_type: str = "code", **extra_params
    ) -> str:
        """Compose the authorization endpoint query string.
        Override in provider‑specific subclasses if needed.
        """
        params = {
            "response_type": response_type,
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            **extra_params,
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.base_url}/oauth2/authorize?{query}"

    def exchange_code_for_tokens(
        self, code: str, redirect_uri: str, **extra_params
    ) -> Dict[str, Any]:
        """Exchange an authorization code for access/refresh tokens.
        Override in provider‑specific subclasses if the request format differs.
        """
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            **extra_params,
        }
        resp = requests.post(f"{self.base_url}/oauth2/token", data=payload)
        resp.raise_for_status()
        return resp.json()

    def get_userinfo(self, access_token: str) -> requests.Response:
        """Call the userinfo endpoint to retrieve profile claims.
        Override if the endpoint path differs per provider.
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        return requests.get(f"{self.base_url}/openid/userinfo", headers=headers)
