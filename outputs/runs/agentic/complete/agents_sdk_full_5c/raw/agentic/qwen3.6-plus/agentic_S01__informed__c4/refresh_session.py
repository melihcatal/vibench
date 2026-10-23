"""
Refresh an expired session or access token using Auth0 OAuth2 API.

Uses Auth0 service for token refresh via the /oauth/token endpoint
with the refresh_token grant type.
Auth0 domain: AUTH0_DOMAIN
Auth0 client credentials: AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
Provider: Auth0 Authentication API (auth0.com)
"""

from typing import Optional, Dict, Any, Tuple

import requests

from identity_client import get_identity_config, Auth0Config
from identity_models import (
    RefreshRequest,
    RefreshResponse,
    IdentityError,
)


def refresh_access_token(
    refresh_token: str,
    audience: Optional[str] = None,
    config: Optional[Auth0Config] = None,
) -> Tuple[Optional[RefreshResponse], Optional[IdentityError]]:
    """
    Refresh an expired access token using a valid refresh token via Auth0.

    POST https://{AUTH0_DOMAIN}/oauth/token
    Grant type: refresh_token

    Returns new tokens on success, or an error on failure.
    """
    if config is None:
        config = get_identity_config()

    if not config.is_configured:
        return None, IdentityError(
            error_code="CONFIGURATION_ERROR",
            error_description="Auth0 domain and client ID must be configured",
            status_code=500,
        )

    request = RefreshRequest(
        refresh_token=refresh_token,
        client_id=config.client_id,
    )

    url = f"https://{config.domain}/oauth/token"

    payload = request.to_auth0_payload()
    payload["client_id"] = config.client_id
    payload["client_secret"] = config.client_secret
    if audience or config.api_audience:
        payload["audience"] = audience or config.api_audience

    try:
        response = requests.post(url, json=payload, headers={
            "Content-Type": "application/json",
        }, timeout=30)

        response.raise_for_status()
        data = response.json()
        refresh_result = RefreshResponse.from_auth0_response(data)
        return refresh_result, None
    except requests.exceptions.HTTPError:
        status_code = response.status_code
        try:
            error_data = response.json()
        except ValueError:
            error_data = {"error": "http_error", "error_description": str(response.text)}
        return None, IdentityError.from_auth0_error(error_data, status_code)
    except requests.exceptions.RequestException as exc:
        return None, IdentityError(
            error_code="NETWORK_ERROR",
            error_description=str(exc),
            status_code=503,
        )


def rotate_refresh_token(
    refresh_token: str,
    config: Optional[Auth0Config] = None,
) -> Tuple[Optional[RefreshResponse], Optional[IdentityError]]:
    """
    Refresh tokens and obtain a new refresh token (rotation) via Auth0.

    Auth0 will issue a new refresh token if refresh token rotation
    is enabled in the Auth0 tenant settings.
    """
    return refresh_access_token(refresh_token, config=config)
