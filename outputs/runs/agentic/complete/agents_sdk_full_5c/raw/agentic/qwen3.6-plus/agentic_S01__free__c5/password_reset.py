"""
Start a password reset flow for a local Auth0 account.
Uses the Auth0 Authentication API /dbconnections/change_password endpoint
to trigger an email with a password change link for the user.
"""

import os
import requests
from typing import Optional

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_DATABASE_CONNECTION,
    build_auth0_reset_password_url,
)
from identity_models import PasswordResetRequest, PasswordResetResponse, normalize_auth_error


def start_password_reset(
    email: str,
    connection: Optional[str] = None,
    client_id: Optional[str] = None,
) -> PasswordResetResponse:
    """
    Initiate a password reset for an Auth0 user by sending a reset email.

    Calls Auth0 /dbconnections/change_password which triggers Auth0 to
    send an email to the user with a password change link.

    Args:
        email: The email address of the account to reset.
        connection: Auth0 database connection name.
        client_id: Auth0 application client ID.

    Returns:
        PasswordResetResponse confirming the reset email was initiated.

    Raises:
        Exception: If the reset request fails.
    """
    conn = connection or AUTH0_DATABASE_CONNECTION
    cid = client_id or AUTH0_CLIENT_ID

    request = PasswordResetRequest(
        email=email,
        connection=conn,
        client_id=cid,
    )

    payload = request.to_auth0_payload()

    reset_url = build_auth0_reset_password_url()

    response = requests.post(
        reset_url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    if response.status_code in (200, 201):
        return PasswordResetResponse.from_auth0_response(response.json())

    error = normalize_auth_error(response.json())
    raise Exception(
        f"Auth0 password reset failed: {error['error']} - {error['error_description']}"
    )


if __name__ == "__main__":
    result = start_password_reset(
        email=os.getenv("RESET_EMAIL", "user@example.com"),
    )
    print(f"Password reset initiated for: {result.email} (status: {result.reset_status})")
