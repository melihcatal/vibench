import os
from typing import Optional, List
import json

class IdentityClientConfig:
    """Local configuration for identity provider integration."""
    def __init__(
        self,
        client_id: str,
        client_secret: Optional[str] = None,
        redirect_uri: str = "",
        scopes: Optional[List[str]] = None,
        issuer: Optional[str] = None,
        auth_uri: Optional[str] = None,
        token_uri: Optional[str] = None,
        userinfo_uri: Optional[str] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes if scopes is not None else []
        self.issuer = issuer
        self.auth_uri = auth_uri
        self.token_uri = token_uri
        self.userinfo_uri = userinfo_uri

    @classmethod
    def from_env_google(cls):
        return cls(
            client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
            client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", None),
            redirect_uri=os.environ.get("GOOGLE_REDIRECT_URI", ""),
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            issuer="https://accounts.google.com",
            auth_uri="https://accounts.google.com/o/oauth2/auth",
            token_uri="https://oauth2.googleapis.com/token",
            userinfo_uri="https://www.googleapis.com/oauth2/v3/userinfo",
        )

    def to_client_secrets_json(self, path: str = "client_secret.json"): # For google_auth_oauthlib
        data = {
            "web": {
                "client_id": self.client_id,
                "project_id": "local-project-id", # Placeholder
                "auth_uri": self.auth_uri,
                "token_uri": self.token_uri,
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", # Google specific
                "client_secret": self.client_secret or "",
                "redirect_uris": [self.redirect_uri]
            }
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


class IdentityClient:
    """Helper utilities for Federated Login Flow client operations."""
    def __init__(self, config: IdentityClientConfig):
        self.config = config

    # Add other common client methods here as needed, e.g., token refresh
