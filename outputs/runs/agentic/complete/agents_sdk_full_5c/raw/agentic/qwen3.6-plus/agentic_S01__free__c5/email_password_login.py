"""
Sign in a user with email and password and return tokens.
Uses the Auth0 Authentication API /oauth/token endpoint with the
Resource Owner Password Credentials (password) grant type.
"""

import os
import requests
from typing import Optional

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_AUDIENCE,
    AUTH0_DATABASE_CONNECTION,
    build_auth0_token_url,
)
from identity_models import LoginRequest, TokenResponse, normalize_auth_error


def email_password_login(
    email: str,
    password: str,
    audience: Optional[str] = None,
    scope: str = "openid profile email",
    connection: Optional[str] = None,
) -> TokenResponse:
    """
    Authenticate a user with email and password against Auth0 and return tokens.

    Uses the Auth0 Authentication API's password grant to obtain
    access_token, id_token, and optionally refresh_token.

    Args:
        email: User's email address.
        password: User's password.
        audience: Target API audience identifier (defaults to Auth0 Management API).
        scope: OIDC scope string (defaults to openid profile email).
        connection: Auth0 database connection name.

    Returns:
        TokenResponse containing access_token, id_token, and refresh_token.

    Raises:
        Exception: If authentication fails.
    """
    conn = connection or AUTH0_DATABASE_CONNECTION
    aud = audience or AUTH0_AUDIENCE

    request = LoginRequest(
        email=email,
        password=password,
        audience=aud,
        scope=scope,
        grant_type="password",
        client_id=AUTH0_CLIENT_ID,
        connection=conn,
    )

    payload = request.to_auth0_payload()
    if AUTH0_CLIENT_SECRET:
        payload["client_secret"] = AUTH0_CLIENT_SECRET

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
        f"Auth0 login failed: {error['error']} - {error['error_description']}"
    )


if __name__ == "__main__":
    tokens = email_password_login(
        email=os.getenv("TEST_USER_EMAIL", "user@example.com"),
        password=os.getenv("TEST_USER_PASSWORD", "password123"),
    )
    print(f"Access token: {tokens.access_token[:20]}...")
    print(f"ID token: {tokens.id_token[:20]}...")
    if tokens.refresh_token:
        print(f"Refresh token: {tokens.refresh_token[:20]}...")
