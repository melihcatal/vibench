"""
Sign in a user with email and password and return tokens via Auth0.

Uses Auth0's Resource Owner Password Credentials (ROPC) grant through
the AuthenticationClient to authenticate and obtain access/id/refresh tokens.
Provider: Auth0 (auth0.com) with auth0-python SDK.
"""

from typing import Optional

from identity_client import Auth0Config, build_auth0_clients
from identity_models import LoginRequest, LoginResponse, normalize_user_email


def email_password_login(
    email: str,
    password: str,
    config: Optional[Auth0Config] = None,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> LoginResponse:
    """
    Authenticate a user with email and password against Auth0 and
    return an access token, id token, and optional refresh token.

    Uses the Auth0 AuthenticationClient.login method which calls
    POST https://{domain}/oauth/token with grant_type=password.

    Args:
        email: User's email address.
        password: User's password.
        config: Auth0Config; falls back to environment variables.
        audience: API audience for the access token.
        scope: OIDC scopes to request.

    Returns:
        LoginResponse with access_token, id_token, refresh_token, etc.

    Raises:
        auth0.exceptions.AuthenticationError: On invalid credentials.
    """
    if config is None:
        config = Auth0Config()
    config.validate()

    auth_client, _ = build_auth0_clients(config)

    normalized_email = normalize_user_email(email)
    api_audience = audience or config.api_audience
    requested_scope = scope or "openid profile email"

    request = LoginRequest(
        email=normalized_email,
        password=password,
        audience=api_audience,
        scope=requested_scope,
    )

    # Auth0 AuthenticationClient.login calls
    # POST https://{domain}/oauth/token with grant_type=password
    raw_response = auth_client.login(
        username=normalized_email,
        password=password,
        realm=config.database_connection,
        audience=api_audience,
        scope=requested_scope,
    )

    response = LoginResponse.from_auth0_response(raw_response)
    return response
