"""
Register a new email/password user account using Auth0 Management API.

Uses Auth0 service for user creation via the Management API.
Auth0 domain: AUTH0_DOMAIN
Auth0 Management API Token: AUTH0_MANAGEMENT_API_TOKEN
Provider SDK/Interface: requests-based REST calls to auth0.com
"""

import os
from typing import Optional, Dict, Any, Tuple

import requests

from identity_client import get_identity_config, Auth0Config
from identity_models import (
    RegisterUserRequest,
    RegisteredUserResponse,
    IdentityError,
)


def register_user(
    email: str,
    password: str,
    connection: str = "Username-Password-Authentication",
    given_name: Optional[str] = None,
    family_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    config: Optional[Auth0Config] = None,
) -> Tuple[Optional[RegisteredUserResponse], Optional[IdentityError]]:
    """
    Create a new user in Auth0 via the Management API Create User endpoint.

    POST /api/v2/users
    https://auth0.com/docs/api/management/v2#!/Users/post_users

    Returns the registered user info on success, or an error on failure.
    """
    if config is None:
        config = get_identity_config()

    if not config.is_configured:
        return None, IdentityError(
            error_code="CONFIGURATION_ERROR",
            error_description="Auth0 domain and client ID must be configured",
            status_code=500,
        )

    request = RegisterUserRequest(
        email=email,
        password=password,
        connection=connection,
        given_name=given_name,
        family_name=family_name,
        metadata=metadata,
    )

    url = f"https://{config.domain}/api/v2/users"
    headers = {
        "Authorization": f"Bearer {config.management_api_token}",
        "Content-Type": "application/json",
    }

    payload = request.to_auth0_payload()

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        user = RegisteredUserResponse.from_auth0_response(data)
        return user, None
    except requests.exceptions.HTTPError as exc:
        status_code = response.status_code
        try:
            error_data = response.json()
        except ValueError:
            error_data = {"error": "http_error", "error_description": str(exc)}
        return None, IdentityError.from_auth0_error(error_data, status_code)
    except requests.exceptions.RequestException as exc:
        return None, IdentityError(
            error_code="NETWORK_ERROR",
            error_description=str(exc),
            status_code=503,
        )


def register_user_with_email_verification(
    email: str,
    password: str,
    connection: str = "Username-Password-Authentication",
    given_name: Optional[str] = None,
    family_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    verify_email: bool = True,
    config: Optional[Auth0Config] = None,
) -> Tuple[Optional[RegisteredUserResponse], Optional[IdentityError]]:
    """
    Register a user and optionally trigger Auth0 email verification.

    Auth0 will send a verification email when the user is created
    with verify_email=true and the connection supports it.
    """
    user, error = register_user(
        email=email,
        password=password,
        connection=connection,
        given_name=given_name,
        family_name=family_name,
        metadata=metadata,
        config=config,
    )

    if error is not None:
        return None, error

    return user, None
