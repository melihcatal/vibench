import os
import base64
import hashlib
import requests
from urllib.parse import urlencode
from identity_client import get_identity_client
from identity_models import OAuthConfig, PKCERequest, TokenResponse

# Using Auth0 as the OAuth/OIDC provider
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:3000/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")


def generate_pkce_pair() -> PKCERequest:
    """Generates PKCE code verifier and challenge."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge).decode("utf-8").rstrip("=")
    )

    return PKCERequest(code_verifier=code_verifier, code_challenge=code_challenge)


def start_pkce_login(state: str, redirect_uri: str = None) -> tuple[str, PKCERequest]:
    """Starts a PKCE login flow with Auth0."""
    config = OAuthConfig(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        callback_url=redirect_uri or AUTH0_CALLBACK_URL,
        audience=AUTH0_AUDIENCE,
        scope=AUTH0_SCOPE,
    )

    pkce = generate_pkce_pair()

    query_params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.callback_url,
        "scope": config.scope,
        "audience": config.audience,
        "state": state,
        "code_challenge": pkce.code_challenge,
        "code_challenge_method": "S256",
    }

    auth_url = f"https://{config.domain}/authorize?{urlencode(query_params)}"
    return auth_url, pkce


def exchange_pkce_code_for_tokens(
    code: str, pkce: PKCERequest, redirect_uri: str = None
) -> TokenResponse:
    """Exchanges a PKCE authorization code for tokens."""
    config = OAuthConfig(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        callback_url=redirect_uri or AUTH0_CALLBACK_URL,
    )

    token_url = f"https://{config.domain}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": config.callback_url,
        "code_verifier": pkce.code_verifier,
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
