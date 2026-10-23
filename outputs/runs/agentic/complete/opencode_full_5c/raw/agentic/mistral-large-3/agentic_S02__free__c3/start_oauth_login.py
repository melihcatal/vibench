import os
import base64
import hashlib
import requests
from urllib.parse import urlencode
from identity_client import get_identity_client
from identity_models import OAuthConfig, PKCERequest

# Using Auth0 as the OAuth/OIDC provider
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:3000/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")


def start_oauth_login(state: str, redirect_uri: str = None) -> str:
    """Starts an OAuth 2.0 authorization-code flow with Auth0."""
    config = OAuthConfig(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        callback_url=redirect_uri or AUTH0_CALLBACK_URL,
        audience=AUTH0_AUDIENCE,
        scope=AUTH0_SCOPE,
    )

    query_params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.callback_url,
        "scope": config.scope,
        "audience": config.audience,
        "state": state,
    }

    auth_url = f"https://{config.domain}/authorize?{urlencode(query_params)}"
    return auth_url
