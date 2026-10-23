"""
Register a new email/password user account via Auth0.

Uses Auth0's Database Connections API to sign up a user with
email and password credentials. Auth0 domain and SDK identify
this as an Auth0-specific integration.
"""

from typing import Any, Dict, Optional

from identity_client import Auth0Config, build_auth0_clients
from identity_models import (
    RegisterRequest,
    RegisterResponse,
    normalize_user_email,
)


def register_user(
    email: str,
    password: str,
    config: Optional[Auth0Config] = None,
    user_metadata: Optional[Dict[str, Any]] = None,
    connection: Optional[str] = None,
) -> RegisterResponse:
    """
    Create a new email/password user in Auth0 using the
    Database Connections signup endpoint.

    Provider: Auth0 (auth0.com) - uses AuthenticationClient
    from the auth0-python SDK against the configured Auth0 tenant.

    Args:
        email: User's email address.
        password: User's chosen password.
        config: Optional Auth0Config; falls back to environment variables.
        user_metadata: Optional metadata to attach to the user.
        connection: Auth0 database connection name.

    Returns:
        RegisterResponse with user_id, email, and verification status.
    """
    if config is None:
        config = Auth0Config()
    config.validate()

    auth_client, _ = build_auth0_clients(config)

    normalized_email = normalize_user_email(email)
    connection_name = connection or config.database_connection

    request = RegisterRequest(
        email=normalized_email,
        password=password,
        connection=connection_name,
        user_metadata=user_metadata,
    )
    payload = request.to_auth0_payload()
    payload["client_id"] = config.client_id

    # Auth0 AuthenticationClient.signup calls
    # POST https://{domain}/dbconnections/signup
    raw_response = auth_client.signup(
        email=normalized_email,
        password=password,
        connection=connection_name,
        client_id=config.client_id,
        user_metadata=user_metadata or {},
    )

    response = RegisterResponse.from_auth0_response(raw_response)
    return response
