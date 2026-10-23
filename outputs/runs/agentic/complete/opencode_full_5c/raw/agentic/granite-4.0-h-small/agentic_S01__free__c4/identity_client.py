import os
import requests


class IdentityClient:
    """Generic client wrapper for identity-related providers."""

    def __init__(self, *args, **kwargs):
        """Initialize with provider-specific configuration.","""
        self.config = kwargs

    def _request(self, method, endpoint, json=None):
        """Perform a HTTP request via the provider API."""
        base_url = self.config.get("base_url", "https://api.provider.com")
        url = f"{base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.config.get('access_token')}",
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, json=json, headers=headers)
        response.raise_for_status()
        return response.json()
