"""
Start a password reset flow for a local account using Auth0 Authentication API.

Uses Auth0 service for password reset via the /dbconnections/change_password
endpoint (for database connections) or /api/v2/tickets/password-change
(Management API ticket-based reset).
Auth0 domain: AUTH0_DOMAIN
Auth0 client credentials: AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
Provider: Auth0 Authentication API (auth0.com)
"""

from typing import Optional, Dict, Any, Tuple

import requests

from identity_client import get_identity_config, Auth0Config
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
    IdentityError,
)


def initiate_password_reset(
    email: str,
    connection: str = "Username-Password-Authentication",
    config: Optional[Auth0Config] = None,
) -> Tuple[Optional[PasswordResetResponse], Optional[IdentityError]]:
    """
    Initiate a password reset email for a user via Auth0's database connection endpoint.

    POST https://{AUTH0_DOMAIN}/dbconnections/change_password

    Auth0 will send a password change email to the user's email address.
    The email contains a link that directs the user to a hosted Auth0 page
    or a custom application page to set a new password.
    """
    if config is None:
        config = get_identity_config()

    if not config.is_configured:
        return None, IdentityError(
            error_code="CONFIGURATION_ERROR",
            error_description="Auth0 domain and client ID must be configured",
            status_code=500,
        )

    request = PasswordResetRequest(
        email=email,
        connection=connection,
        client_id=config.client_id,
    )

    url = f"https://{config.domain}/dbconnections/change_password"

    payload = request.to_auth0_payload()

    try:
        response = requests.post(url, json=payload, headers={
            "Content-Type": "application/json",
        }, timeout=30)

        response.raise_for_status()
        data = response.json()
        result = PasswordResetResponse(
            email=email,
            message=data.get("email", ""),
            success=True,
        )
        return result, None
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


def create_password_change_ticket(
    user_id: str,
    new_password: Optional[str] = None,
    result_url: Optional[str] = None,
    config: Optional[Auth0Config] = None,
) -> Tuple[Optional[PasswordResetResponse], Optional[IdentityError]]:
    """
    Create a password change ticket via Auth0 Management API.

    POST https://{AUTH0_DOMAIN}/api/v2/tickets/password-change

    This is an alternative to the email-based flow that generates
    a one-time URL for the user to set a new password.
    """
    if config is None:
        config = get_identity_config()

    if not config.management_api_token:
        return None, IdentityError(
            error_code="CONFIGURATION_ERROR",
            error_description="Auth0 Management API token must be configured",
            status_code=500,
        )

    url = f"https://{config.domain}/api/v2/tickets/password-change"
    headers = {
        "Authorization": f"Bearer {config.management_api_token}",
        "Content-Type": "application/json",
    }

    payload: Dict[str, Any] = {
        "user_id": user_id,
    }
    if new_password:
        payload["new_password"] = new_password
    if result_url:
        payload["result_url"] = result_url

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        result = PasswordResetResponse(
            email=user_id,
            ticket_url=data.get("ticket_url", data.get("value", "")),
            success=True,
        )
        return result, None
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
