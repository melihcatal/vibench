"""
Start a password reset flow for a local email/password account via Auth0.

Uses Auth0's Database Connections change_password endpoint to trigger
a password reset email to the user's registered email address.
Provider: Auth0 (auth0.com) with auth0-python SDK.
"""

from typing import Optional

from identity_client import Auth0Config, build_auth0_clients
from identity_models import PasswordResetRequest, normalize_user_email


def password_reset(
    email: str,
    config: Optional[Auth0Config] = None,
    connection: Optional[str] = None,
) -> str:
    """
    Initiate a password reset for the given email address via Auth0.

    Uses Auth0's AuthenticationClient.change_password method which calls
    POST https://{domain}/dbconnections/change_password to send a password
    reset email to the user.

    Args:
        email: The email address of the account to reset.
        config: Auth0Config; falls back to environment variables.
        connection: Auth0 database connection name.

    Returns:
        A confirmation string from Auth0 (typically the email address
        that the reset email was sent to).

    Raises:
        auth0.exceptions.AuthenticationError: On invalid request parameters.
    """
    if config is None:
        config = Auth0Config()
    config.validate()

    auth_client, _ = build_auth0_clients(config)

    normalized_email = normalize_user_email(email)
    connection_name = connection or config.database_connection

    request = PasswordResetRequest(
        email=normalized_email,
        connection=connection_name,
        client_id=config.client_id,
    )

    # Auth0 AuthenticationClient.change_password calls
    # POST https://{domain}/dbconnections/change_password
    result = auth_client.change_password(
        email=normalized_email,
        connection=connection_name,
        client_id=config.client_id,
    )

    # Auth0 returns the email address as confirmation string
    confirmation = result if isinstance(result, str) else str(result)
    return confirmation
