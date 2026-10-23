"""
Register a new email/password user account via Auth0 Authentication API.
Uses the Auth0 /dbconnections/signup endpoint to create a user in the
configured database connection.
"""

import os
import requests
from typing import Optional, Dict, Any

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_DATABASE_CONNECTION,
    build_auth0_signup_url,
)
from identity_models import RegistrationRequest, RegistrationResponse, normalize_auth_error


def register_user(
    email: str,
    password: str,
    given_name: str = "",
    family_name: str = "",
    connection: Optional[str] = None,
    user_metadata: Optional[Dict[str, Any]] = None,
) -> RegistrationResponse:
    """
    Register a new user with email and password through Auth0.

    Args:
        email: User's email address.
        password: User's chosen password.
        given_name: Optional given name.
        family_name: Optional family name.
        connection: Auth0 database connection name (defaults to Username-Password-Authentication).
        user_metadata: Optional additional metadata dict.

    Returns:
        RegistrationResponse containing user details.

    Raises:
        Exception: If registration fails.
    """
    conn = connection or AUTH0_DATABASE_CONNECTION

    request = RegistrationRequest(
        email=email,
        password=password,
        given_name=given_name,
        family_name=family_name,
        connection=conn,
        user_metadata=user_metadata or {},
    )

    payload = request.to_auth0_payload()
    payload["client_id"] = AUTH0_CLIENT_ID

    signup_url = build_auth0_signup_url()

    response = requests.post(
        signup_url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    if response.status_code in (200, 201):
        return RegistrationResponse.from_auth0_response(response.json())

    error = normalize_auth_error(response.json())
    raise Exception(
        f"Auth0 registration failed: {error['error']} - {error['error_description']}"
    )


if __name__ == "__main__":
    result = register_user(
        email=os.getenv("TEST_USER_EMAIL", "newuser@example.com"),
        password=os.getenv("TEST_USER_PASSWORD", "S3cureP@ss!"),
        given_name="New",
        family_name="User",
    )
    print(f"Registered user: {result.user_id} ({result.email})")
