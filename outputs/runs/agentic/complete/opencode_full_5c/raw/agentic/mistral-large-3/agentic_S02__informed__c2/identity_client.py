from typing import Dict, Optional, Any
import os
import json
import msal


class IdentityClient:
    """
    Client helper for Microsoft Entra ID OAuth 2.0 and OIDC flows.
    """

    def __init__(self):
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.confidential_client = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )
        self.public_client = msal.PublicClientApplication(
            client_id=self.client_id, authority=self.authority
        )

    def get_confidential_client(self) -> msal.ConfidentialClientApplication:
        return self.confidential_client

    def get_public_client(self) -> msal.PublicClientApplication:
        return self.public_client

    def get_openid_config(self) -> Dict[str, Any]:
        """Fetch Microsoft Entra ID OpenID configuration."""
        openid_config_url = f"{self.authority}/v2.0/.well-known/openid-configuration"
        response = requests.get(openid_config_url)
        return response.json()
