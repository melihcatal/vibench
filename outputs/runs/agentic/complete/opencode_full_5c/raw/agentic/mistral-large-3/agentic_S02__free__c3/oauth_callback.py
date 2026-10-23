import os
import requests
from identity_client import get_identity_client
from identity_models import OAuthConfig, TokenResponse

# Using Auth0 as the OAuth/OIDC provider
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:3000/callback")


def exchange_code_for_tokens(code: str, redirect_uri: str = None) -> TokenResponse:
    """Exchanges an authorization code for tokens using Auth0."""
    config = OAuthConfig(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        callback_url=redirect_uri or AUTH0_CALLBACK_URL,
    )

    token_url = f"https://{config.domain}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": config.callback_url,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()

    token_data = response.json()
    return TokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
    )


def oauth_callback(code: str, state: str) -> TokenResponse:
    """Handles the OAuth callback and exchanges the code for tokens."""
    return exchange_code_for_tokens(code)
