"""
Sign in a user with email and password using Auth0 OAuth2 API.

Uses Auth0 service for authentication via the /oauth/token endpoint
with the password-realm grant type (Resource Owner Password flow).
Auth0 domain: AUTH0_DOMAIN
Auth0 client credentials: AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
Provider: Auth0 Authentication API (auth0.com)
"""

import os
from typing import Optional, Dict, Any, Tuple

import requests

from identity_client import get_identity_config, Auth0Config
from identity_models import (
    LoginRequest,
    LoginResponse,
    IdentityError,
)


def login_with_email_password(
    email: str,
    password: str,
    audience: Optional[str] = None,
    scope: str = "openid profile email",
    config: Optional[Auth0Config] = None,
) -> Tuple[Optional[LoginResponse], Optional[IdentityError]]:
    """
    Authenticate a user against Auth0 using email and password.

    POST https://{AUTH0_DOMAIN}/oauth/token
    Grant type: http://auth0.com/oauth/grant-type/password-realm

    Returns tokens on success, or an error on failure.
    """
    if config is None:
        config = get_identity_config()

    if not config.is_configured:
        return None, IdentityError(
            error_code="CONFIGURATION_ERROR",
            error_description="Auth0 domain and client ID must be configured",
            status_code=500,
        )

    request = LoginRequest(
        email=email,
        password=password,
        audience=audience or config.api_audience,
        scope=scope,
    )

    url = f"https://{config.domain}/oauth/token"

    payload = request.to_auth0_payload()
    payload["client_id"] = config.client_id
    payload["client_secret"] = config.client_secret

    try:
        response = requests.post(url, json=payload, headers={
            "Content-Type": "application/json",
        }, timeout=30)

        response.raise_for_status()
        data = response.json()
        login_result = LoginResponse.from_auth0_response(data)
        return login_result, None
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


def get_user_info(
    access_token: str,
    config: Optional[Auth0Config] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[IdentityError]]:
    """
    Retrieve the authenticated user's profile from Auth0 /userinfo endpoint.

    GET https://{AUTH0_DOMAIN}/userinfo
    Authorization: Bearer {access_token}
    """
    if config is None:
        config = get_identity_config()

    url = f"https://{config.domain}/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json(), None
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
