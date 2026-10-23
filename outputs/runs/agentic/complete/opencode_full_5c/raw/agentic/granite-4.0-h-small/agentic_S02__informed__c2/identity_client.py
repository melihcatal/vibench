import json
import os

# Local identity client utilities and configuration
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
IDENTITY_METADATA = {
    "default_provider": "AzureAD",
    "providers": {
        "AzureAD": {
            "authority": f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0",
            "client_id": AZURE_CLIENT_ID,
            "client_secret": AZURE_CLIENT_SECRET,
        }
    },
}


def config_for_provider(provider_name):
    """
    Returns configuration for the named identity provider.
    Currently supports 'AzureAD'. Extend with other providers as needed.
    """
    return IDENTITY_METADATA["providers"].get(provider_name, None)


class IdentityClient:
    """
    Simple wrapper around MSAL to abstract provider differences.
    """

    def __init__(self, provider_config):
        self.provider = provider_config["name"]
        self.authority = provider_config["authority"]
        self.client_id = provider_config["client_id"]
        self.client_secret = provider_config["client_secret"]
        self.client = None  # will be initialized lazily

    def init_msal(self):
        """
        Initializes MSAL client for the configured provider.
        """
        from msal import ConfidentialClientApplication

        self.client = ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )

    def get_authorization_url(self, redirect_uri, scope=["openid", "profile", "email"]):
        """
        Returns the OIDC authorization URL for public clients.
        """
        if not self.client:
            self.init_msal()
        return self.client.get_authorization_request_url(
            scope, redirect_uri=redirect_uri, response_type="code"
        )

    def exchange_code(self, code, redirect_uri):
        """
        Exchanges an authorization code for tokens.
        """
        if not self.client:
            self.init_msal()
        return self.client.acquire_token_by_authorization_code(
            code, scopes=["openid", "profile", "email"], redirect_uri=redirect_uri
        )

    def fetch_user_profile(self, id_token):
        """
        Basic parser for OIDC id_token claims.
        """
        if not id_token:
            return None
        payload = json.loads(id_token)
        return {
            "sub": payload.get("sub"),
            "email": payload.get("preferred_username") or payload.get("email"),
            "display_name": payload.get("name"),
            "locale": payload.get("locale"),
        }
