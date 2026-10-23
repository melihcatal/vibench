import os
import base64
import hashlib
import secrets
import requests
from urllib.parse import urlencode

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_CALLBACK_URL,
    get_auth0_authorize_url,
    get_auth0_token_url,
)
from identity_models import OAuthTokens


def generate_pkce_codes():
    """Generates PKCE code_verifier and code_challenge.

    Returns:
        A tuple containing (code_verifier, code_challenge).
    """
    code_verifier = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge


def start_pkce_login(redirect_uri: str) -> tuple[str, str]:
    """Starts a PKCE login flow for public clients with Auth0.

    Args:
        redirect_uri: The URI to redirect to after successful authentication.

    Returns:
        A tuple containing the authorization URL and the code_verifier (which must be stored by the client).
    """
    code_verifier, code_challenge = generate_pkce_codes()
    state = secrets.token_urlsafe(16)

    auth_url = get_auth0_authorize_url(redirect_uri, state, code_challenge)
    return auth_url, code_verifier


def exchange_pkce_code_for_tokens(
    code: str, code_verifier: str, redirect_uri: str
) -> OAuthTokens:
    """Exchanges the authorization code for tokens using PKCE with Auth0.

    Args:
        code: The authorization code received from the identity provider.
        code_verifier: The code_verifier generated at the start of the PKCE flow.
        redirect_uri: The original redirect URI used in the authorization request.

    Returns:
        An OAuthTokens object containing the access token, ID token, and other token details.

    Raises:
        Exception: If token exchange fails.
    """
    token_url = get_auth0_token_url()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,  # Although for public clients, client_secret is often not used, Auth0 still expects it if configured.
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()

    return OAuthTokens(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        token_type=token_data.get("token_type"),
        expires_in=token_data.get("expires_in"),
    )
