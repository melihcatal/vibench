"""
Refresh an expired session or access token via Auth0.

Uses Auth0's token endpoint with the refresh_token grant type
to obtain a new access token without requiring re-authentication.
Provider: Auth0 (auth0.com) with auth0-python SDK and direct REST call.
"""

from typing import Optional
import requests

from identity_client import Auth0Config
from identity_models import LoginResponse


def refresh_session(
    refresh_token: str,
    config: Optional[Auth0Config] = None,
) -> LoginResponse:
    """
    Exchange a refresh token for a new set of tokens from Auth0.

    Calls POST https://{domain}/oauth/token with grant_type=refresh_token
    using the Auth0 REST API. The Auth0 domain and tenant-specific
    endpoint identify this as an Auth0-specific integration.

    Args:
        refresh_token: The refresh token obtained during initial login.
        config: Auth0Config; falls back to environment variables.

    Returns:
        LoginResponse with a new access_token, id_token, and optionally
        a new refresh token.

    Raises:
        requests.HTTPError: On invalid or expired refresh token.
    """
    if config is None:
        config = Auth0Config()
    config.validate()

    # Auth0 REST token endpoint for refresh_token grant
    token_url = f"https://{config.domain}/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": config.client_id,
        "refresh_token": refresh_token,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()

    raw_response = response.json()
    return LoginResponse.from_auth0_response(raw_response)
