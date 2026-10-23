import os
from typing import TypedDict
from identity_models import ProviderConfiguration

# Central location for client configuration and helper utilities
# Provider identifiers are present as constants


class IdentityClientConfig(TypedDict):
    api_base_url: str
    access_token: str
    refresh_token: str | None
    client_id: str
    client_secret: str | None
    token_endpoint: str | None
    userinfo_endpoint: str | None
    authorize_url: str
    identity_provider: str


# Example Google Identity Platform configuration
GOOGLE_CONFIG: IdentityClientConfig = {
    "api_base_url": "https://accounts.google.com",
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    "token_endpoint": "https://oauth2.googleapis.com/token",
    "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
    "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
    "identity_provider": "Google Identity Platform",
}

# Example Auth0 configuration (PKCE flow)
AUTH0_CONFIG: IdentityClientConfig = {
    "api_base_url": "https://YOUR_AUTH0_DOMAIN.auth0.com",
    "client_id": os.getenv("AUTH0_CLIENT_ID"),
    "client_secret": None,  # public client does not have secret
    "token_endpoint": "https://YOUR_AUTH0_DOMAIN.auth0.com/oauth/token",
    "userinfo_endpoint": "https://YOUR_AUTH0_DOMAIN.auth0.comuserinfo",
    "authorize_url": "https://YOUR_AUTH0_DOMAIN.auth0.com/authorize",
    "identity_provider": "Auth0",
}


def get_client(provider_key: str) -> IdentityClient:
    """Factory to return an IdentityClient pre‑configured with provider‑specific settings.","""
    config_map = {
        "google": GOOGLE_CONFIG,
        "auth0": AUTH0_CONFIG,
        "cognito": None,  # placeholder
        "microsoft": None,
        "ibm": None,
    }
    cfg = config_map.get(provider_key.lower())
    if not cfg:
        raise ValueError(f"Unsupported provider: {provider_key}")
    return IdentityClient(**cfg)
