"""
Refresh an expired session or access token via Auth0.
Uses the Auth0 Authentication API /oauth/token endpoint with the
refresh_token grant type to obtain new tokens.
"""

import os
import requests
from typing import Optional

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    build_auth0_token_url,
)
from identity_models import RefreshRequest, TokenResponse, normalize_auth_error


def refresh_session(
    refresh_token: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    scope: Optional[str] = None,
) -> TokenResponse:
    """
    Refresh an expired Auth0 session using a refresh token.

    Calls Auth0 /oauth/token with grant_type=refresh_token to obtain
    a new access token and optionally a new refresh token (when
    offline_access scope was originally granted).

    Args:
        refresh_token: The refresh token from a prior authentication.
        client_id: Auth0 client ID (defaults to AUTH0_CLIENT_ID).
        client_secret: Auth0 client secret (if required for token endpoint).
        scope: Optional space-delimited scope string.

    Returns:
        TokenResponse with fresh access_token and id_token.

    Raises:
        Exception: If refresh fails.
    """
    cid = client_id or AUTH0_CLIENT_ID
    csecret = client_secret or AUTH0_CLIENT_SECRET

    request = RefreshRequest(
        refresh_token=refresh_token,
        grant_type="refresh_token",
        client_id=cid,
    )

    payload = request.to_auth0_payload()
    if csecret:
        payload["client_secret"] = csecret
    if scope:
        payload["scope"] = scope

    token_url = build_auth0_token_url()

    response = requests.post(
        token_url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    if response.status_code == 200:
        return TokenResponse.from_auth0_response(response.json())

    error = normalize_auth_error(response.json())
    raise Exception(
        f"Auth0 token refresh failed: {error['error']} - {error['error_description']}"
    )


if __name__ == "__main__":
    old_refresh_token = os.getenv("REFRESH_TOKEN", "")
    if not old_refresh_token:
        print("No refresh token provided. Set REFRESH_TOKEN env var.")
    else:
        new_tokens = refresh_session(refresh_token=old_refresh_token)
        print(f"New access token: {new_tokens.access_token[:20]}...")
