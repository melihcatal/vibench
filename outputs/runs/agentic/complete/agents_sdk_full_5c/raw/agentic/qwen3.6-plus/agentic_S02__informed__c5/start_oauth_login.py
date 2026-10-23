"""Start an OAuth/OIDC authorization-code login with Auth0.

This module initiates the authorization-code flow by constructing
the Auth0 authorization endpoint URL with required parameters.

Provider: Auth0 Authentication API
SDK: requests / OIDC protocol
Auth env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID
"""

import os
from typing import Optional

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_CALLBACK_URL,
    AUTH0_SCOPE,
    AUTH0_AUDIENCE,
    build_authorization_url,
    generate_state,
)


def start_oauth_login(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    response_mode: Optional[str] = None,
    prompt: Optional[str] = None,
    connection: Optional[str] = None,
) -> dict:
    """Initiate an OAuth2 authorization-code login with Auth0.

    Constructs the authorization URL for the Auth0 hosted login page
    and returns the URL along with the generated state parameter.

    Args:
        client_id: Auth0 Application Client ID (falls back to AUTH0_CLIENT_ID).
        redirect_uri: Callback URL after authentication.
        scope: OIDC scopes to request.
        audience: Auth0 API audience identifier.
        response_mode: Response mode (e.g., 'query' or 'form_post').
        prompt: Prompt parameter (e.g., 'login', 'consent', 'none').
        connection: Specific Auth0 connection to use.

    Returns:
        dict with 'authorization_url' and 'state' keys.
    """
    state = generate_state()

    authorization_url = build_authorization_url(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
        audience=audience,
    )

    if response_mode:
        authorization_url += f"&response_mode={response_mode}"
    if prompt:
        authorization_url += f"&prompt={prompt}"
    if connection:
        authorization_url += f"&connection={connection}"

    return {
        "authorization_url": authorization_url,
        "state": state,
        "client_id": client_id or AUTH0_CLIENT_ID,
        "provider": "Auth0",
    }


def start_oauth_login_with_custom_params(
    extra_params: Optional[dict] = None,
) -> dict:
    """Start OAuth login with additional custom Auth0 parameters.

    Args:
        extra_params: Additional query parameters for Auth0 authorization endpoint.

    Returns:
        dict with 'authorization_url' and 'state' keys.
    """
    state = generate_state()

    authorization_url = build_authorization_url(
        state=state,
    )

    if extra_params:
        for key, value in extra_params.items():
            authorization_url += f"&{key}={value}"

    return {
        "authorization_url": authorization_url,
        "state": state,
        "provider": "Auth0",
    }


if __name__ == "__main__":
    result = start_oauth_login()
    print(f"Authorization URL: {result['authorization_url']}")
    print(f"State: {result['state']}")
