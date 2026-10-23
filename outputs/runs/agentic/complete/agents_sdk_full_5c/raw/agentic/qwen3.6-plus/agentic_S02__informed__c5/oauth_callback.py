"""Handle the Auth0 OAuth/OIDC callback and exchange authorization code for tokens.

This module processes the callback from Auth0, validates the state parameter,
and exchanges the authorization code for access, ID, and refresh tokens.

Provider: Auth0 Authentication API
SDK: requests
Auth env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
"""

import os
import requests
from typing import Optional

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_TOKEN_ENDPOINT,
    AUTH0_CALLBACK_URL,
    validate_state,
)
from identity_models import TokenResponse


def handle_callback(
    authorization_code: str,
    state: str,
    expected_state: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    """Handle the Auth0 OAuth callback and exchange code for tokens.

    Validates the state parameter and exchanges the authorization code
    for tokens using the Auth0 /oauth/token endpoint.

    Args:
        authorization_code: The authorization code from Auth0 callback.
        state: The state parameter received in the callback.
        expected_state: The original state generated during login initiation.
        client_id: Auth0 Client ID (falls back to AUTH0_CLIENT_ID).
        client_secret: Auth0 Client Secret (falls back to AUTH0_CLIENT_SECRET).
        redirect_uri: The redirect URI used in the authorization request.
        code_verifier: PKCE code verifier if PKCE was used.

    Returns:
        TokenResponse with the exchanged tokens.

    Raises:
        ValueError: If state validation fails or required parameters are missing.
        requests.RequestException: If the token exchange request fails.
    """
    if not validate_state(state, expected_state):
        raise ValueError("State parameter validation failed - possible CSRF attack")

    if not AUTH0_TOKEN_ENDPOINT:
        raise ValueError("AUTH0_DOMAIN environment variable is not set")

    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri or AUTH0_CALLBACK_URL,
        "client_id": client_id or AUTH0_CLIENT_ID or "",
        "client_secret": client_secret or AUTH0_CLIENT_SECRET or "",
    }

    if code_verifier:
        token_data["code_verifier"] = code_verifier

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(
        AUTH0_TOKEN_ENDPOINT,
        data=token_data,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    token_json = response.json()
    return TokenResponse.from_auth0_response(token_json)


def exchange_token_for_auth0_api(
    authorization_code: str,
    state: str,
    expected_state: str,
    audience: Optional[str] = None,
) -> TokenResponse:
    """Exchange authorization code for tokens targeting a specific Auth0 API audience.

    Args:
        authorization_code: The authorization code from Auth0 callback.
        state: The state parameter received in the callback.
        expected_state: The original state generated during login initiation.
        audience: The Auth0 API audience to request tokens for.

    Returns:
        TokenResponse with the exchanged tokens.
    """
    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "client_id": AUTH0_CLIENT_ID or "",
        "client_secret": AUTH0_CLIENT_SECRET or "",
    }

    if audience:
        token_data["audience"] = audience

    response = requests.post(
        AUTH0_TOKEN_ENDPOINT,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()

    return TokenResponse.from_auth0_response(response.json())


if __name__ == "__main__":
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else "demo_code"
    st = sys.argv[2] if len(sys.argv) > 2 else "demo_state"
    try:
        result = handle_callback(code, st, st)
        print(f"Access token: {result.access_token[:20]}...")
    except Exception as e:
        print(f"Error: {e}")
