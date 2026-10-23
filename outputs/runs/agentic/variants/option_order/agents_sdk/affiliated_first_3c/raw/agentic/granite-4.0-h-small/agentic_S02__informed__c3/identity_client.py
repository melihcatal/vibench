import os
from typing import Any
import requests

class IdentityClient:
    """Small wrapper to centralize provider credentials and request helpers."""
    # Auth0 settings loaded from env vars
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

    @staticmethod
    def _api_get(url: str, headers: dict[str, str] = None, params: dict[str, Any] = None) -> requests.Response:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp

    @staticmethod
    def _api_post(url: str, data: dict = None, headers: dict = None) -> requests.Response:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
        return resp

    # Example utility to fetch a userinfo endpoint (used by profile_claims)
    @staticmethod
    def fetch_userinfo(access_token: str):
        domain = IdentityClient.AUTH0_DOMAIN
        url = f"https://{domain}/userinfo"
        resp = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
        resp.raise_for_status()
        return resp.json()
