import os
import json
from typing import Any, Dict


class IdentityClient:
    """
    Central helper for interacting with external identity providers.
    Provides uniform config loading and request/response handling.
    """

    def __init__(self):
        # Load generic provider config from environment variables
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        # Optional additional configs (Google, Auth0, etc.) can be added here
        self._token_cache: Dict[str, Any] = {}

    def _build_authority(self) -> str:
        return f"https://login.microsoftonline.com/{self.tenant_id}"

    def get_authorization_url(self, scopes: list[str], redirect_uri: str) -> str:
        """Return an OAuth authorization URL for Microsoft Entra ID."""
        from msal import ConfidentialClientApplication

        client = ConfidentialClientApplication(
            self.client_id, authority=self._build_authority()
        )
        return client.get_authorization_request_url(scopes, redirect_uri=redirect_uri)

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for tokens using the client secret flow."""
        from msal import ConfidentialClientApplication

        client = ConfidentialClientApplication(
            self.client_id,
            authority=self._build_authority(),
            client_credential=self.client_secret,
        )
        return client.acquire_token_by_authorization_code(
            code, scopes=["profile openid"], redirect_uri=redirect_uri
        )

    def fetch_userinfo(self, access_token: str) -> Dict[str, Any]:
        """Call the Microsoft Graph /me endpoint to retrieve user profile."""
        import requests

        url = "https://graph.microsoft.com/v1.0/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    # Additional methods for Google, Auth0, etc. would follow the same pattern
