import os
from typing import Dict, Any, Optional
from authlib.integrations.requests_client import OAuth2Session

# Auth0 and Okta Provider Configurations
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")

OKTA_DOMAIN = os.getenv("OKTA_DOMAIN", "your-org.okta.com")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID", "your-client-id")
OKTA_CALLBACK_URL = os.getenv("OKTA_CALLBACK_URL", "http://localhost:5000/callback")


class IdentityClient:
    def __init__(self, provider: str = "auth0"):
        self.provider = provider
        self._configure_provider()

    def _configure_provider(self):
        if self.provider == "auth0":
            self.domain = AUTH0_DOMAIN
            self.client_id = AUTH0_CLIENT_ID
            self.client_secret = AUTH0_CLIENT_SECRET
            self.callback_url = AUTH0_CALLBACK_URL
            self.authorization_base_url = f"https://{self.domain}/authorize"
            self.token_url = f"https://{self.domain}/oauth/token"
        elif self.provider == "okta":
            self.domain = OKTA_DOMAIN
            self.client_id = OKTA_CLIENT_ID
            self.client_secret = None
            self.callback_url = OKTA_CALLBACK_URL
            self.authorization_base_url = (
                f"https://{self.domain}/oauth2/default/v1/authorize"
            )
            self.token_url = f"https://{self.domain}/oauth2/default/v1/token"

    def get_oauth_session(self, **kwargs) -> OAuth2Session:
        return OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.callback_url,
            **kwargs,
        )

    def get_provider_name(self) -> str:
        return self.provider
