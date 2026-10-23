# identity_client.py
# HELPER: Central configuration & client utility for Federated Login Flow

import os
import json
import urllib.parse
import requests
from typing import Any, Dict

# Dummy provider identifiers – can switch to any SaaS provider SDK (e.g., Auth0, Okta, Google, Azure AD)
DEFAULT_PROVIDER = os.getenv("FEDERATED_PROVIDER", "google")


class IdentityClient:
    """
    Thin wrapper that hides provider‑specific details behind a small set of helpers.

    Usage example:
        client = IdentityClient()
        token = client.post(url="https://auth.example.com/token", json={...})
    """

    def __init__(self):
        self.base_url = self._resolve_base_url()
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _resolve_base_url(self) -> str:
        if DEFAULT_PROVIDER == "google":
            return "https://oauth2.googleapis.com"
        elif DEFAULT_PROVIDER == "okta":
            # Example Okta tenant URL – replace with actual tenant URL
            tenant = os.getenv("OKTA_TENANT_URL")
            return f"https://{tenant}.okta.com"
        else:
            raise NotImplementedError(
                f"Provider {DEFAULT_PROVIDER} base URL not configured"
            )

    def get(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def post(self, url: str, json: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        resp = self.session.post(url, json=json, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def verify_google_id_token(self, id_token: str) -> Dict[str, Any]:
        """
        Minimal wrapper around Google Identity Platform verification.
        In production use google-auth library or cloud function; here we show a
        direct request to the verify endpoint for demonstration.
        """
        verify_url = f"{self.base_url}/tokeninfo"
        params = {"id_token": id_token}
        r = self.session.get(verify_url, params=params)
        r.raise_for_status()
        return r.json()

    def exchange_code(
        self, token_url: str, token_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform a standard authorization‑code exchange (used by both regular and PKCE flows)."""
        return self.post(url=token_url, json=token_request)


# Example instantiation & call for local testing
if __name__ == "__main__":
    client = IdentityClient()
    # Simple health‑check against the provider's tokeninfo endpoint (Google)
    if DEFAULT_PROVIDER == "google":
        print("Provider base URL:", client.base_url)
    else:
        print("Base URL for provider", DEFAULT_PROVIDER, "is", client.base_url)
