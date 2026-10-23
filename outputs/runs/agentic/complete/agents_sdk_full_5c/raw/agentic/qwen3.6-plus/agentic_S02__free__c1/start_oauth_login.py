"""
Start an OAuth/OIDC authorization-code login flow using Auth0.

Constructs the authorization URL with required OAuth 2.0 parameters
and redirects the user to the Auth0 /authorize endpoint. Supports
standard OIDC parameters including nonce, state, scope, audience,
and optional connection selection.
"""

import os
from typing import Optional

from identity_models import (
    OAuthAuthorizationRequest,
    generate_nonce,
    generate_state,
)
from identity_client import (
    AUTH0_AUTHORIZE_URL,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
    AUTH0_AUDIENCE,
)


def start_oauth_login(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: str = "openid profile email",
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    audience: Optional[str] = None,
    connection: Optional[str] = None,
    prompt: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> OAuthAuthorizationRequest:
    """
    Start an OAuth 2.0 / OIDC authorization-code login against Auth0.

    Constructs an OAuthAuthorizationRequest with Auth0-specific
    defaults and generates a secure state and nonce for CSRF and
    replay-attack protection.

    Args:
        client_id: Auth0 Application Client ID.
        redirect_uri: Registered callback URL for this Auth0 application.
        scope: OIDC scopes to request (default: openid profile email).
        state: Optional opaque state value for CSRF protection.
        nonce: Optional nonce for OIDC ID token replay protection.
        audience: Optional Auth0 API audience identifier.
        connection: Optional Auth0 connection name (e.g., "google-oauth2").
        prompt: Optional prompt parameter (e.g., "login", "consent").
        extra_params: Additional query parameters to append.

    Returns:
        OAuthAuthorizationRequest ready to be serialized to an Auth0
        authorization URL.
    """
    cid = client_id or AUTH0_CLIENT_ID
    ruri = redirect_uri or AUTH0_REDIRECT_URI
    aud = audience or AUTH0_AUDIENCE
    st = state or generate_state()
    nc = nonce or generate_nonce()

    request = OAuthAuthorizationRequest(
        client_id=cid,
        redirect_uri=ruri,
        response_type="code",
        scope=scope,
        state=st,
        nonce=nc,
        audience=aud,
        connection=connection,
        prompt=prompt,
    )

    return request


def build_auth0_authorize_url(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: str = "openid profile email",
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    audience: Optional[str] = None,
    connection: Optional[str] = None,
    prompt: Optional[str] = None,
) -> dict:
    """
    Build the full Auth0 /authorize URL and return metadata.

    Returns a dictionary with the authorization URL and the generated
    state/nonce values that must be stored server-side for callback
    verification.
    """
    request = start_oauth_login(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
        nonce=nonce,
        audience=audience,
        connection=connection,
        prompt=prompt,
    )

    authorize_url = request.to_url(AUTH0_AUTHORIZE_URL)

    return {
        "authorize_url": authorize_url,
        "state": request.state,
        "nonce": request.nonce,
        "auth0_domain": os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com"),
        "client_id": request.client_id,
    }


def start_login_with_connection(
    connection: str,
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: str = "openid profile email",
) -> dict:
    """
    Start an Auth0 login flow targeting a specific connection
    (e.g., google-oauth2, github, okta).

    The connection parameter maps to the Auth0 connection name
    configured in the Auth0 dashboard under Identity Providers.
    """
    return build_auth0_authorize_url(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        connection=connection,
    )


if __name__ == "__main__":
    result = build_auth0_authorize_url()
    print(f"Auth0 Authorize URL: {result['authorize_url']}")
    print(f"State: {result['state']}")
    print(f"Nonce: {result['nonce']}")
