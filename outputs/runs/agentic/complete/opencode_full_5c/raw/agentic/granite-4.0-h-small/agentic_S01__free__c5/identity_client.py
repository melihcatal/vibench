import os
import requests
from typing import Any, Dict

# ---------------------------------------------------------------------------
# Provider configuration and HTTP helper
# ---------------------------------------------------------------------------


class IdentityClient:
    """Thin wrapper around the third‑party AuthService SaaS HTTP API.
    All endpoint callers instantiate this client to keep provider details centralized.
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        # Keep the key with the provider‑specific header it expects
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def post(self, path: str, json: Dict[str, Any], **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        # DEBUG logging can be added here if needed
        return self.session.post(url, json=json, **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.get(url, **kwargs)

    # Add other HTTP verbs (put, delete) as required
