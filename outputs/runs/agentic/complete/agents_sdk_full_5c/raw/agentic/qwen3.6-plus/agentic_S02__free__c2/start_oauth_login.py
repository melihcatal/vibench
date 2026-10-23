"""
start_oauth_login.py - Starts an OAuth/OIDC authorization-code login flow
Provider: Auth0 (auth0.com)
"""

import os
import secrets
import urllib.parse
from typing import Optional

from identity_client import get_auth0_config
from identity_models import OAuthLoginRequest, OAuthLoginResponse, generate_state


AUTH0_AUTHORIZE_URL = "https://{domain}/authorize"


def build_authorization_url(
    redirect_uri: str,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    connection: Optional[str] = None,
) -> OAuthLoginResponse:
    """
    Build an Auth0 authorization URL for the authorization-code flow.

    Uses Auth0's OIDC-compliant /authorize endpoint.
    See: https://auth0.com/docs/api/authentication#authorize-application
    """
    config = get_auth0_config()
    domain = config["auth0_domain"]
    client_id = config["auth0_client_id"]

    effective_scope = scope or "openid profile email"
    effective_state = state or generate_state()
    effective_nonce = nonce or secrets.token_urlsafe(32)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": effective_scope,
        "state": effective_state,
        "nonce": effective_nonce,
    }

    if audience:
        params["audience"] = audience
    if connection:
        params["connection"] = connection

    authorize_url = AUTH0_AUTHORIZE_URL.format(domain=domain)
    full_url = f"{authorize_url}?{urllib.parse.urlencode(params)}"

    login_request = OAuthLoginRequest(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=effective_scope,
        state=effective_state,
        nonce=effective_nonce,
        audience=audience,
        connection=connection,
        authorize_url=full_url,
    )

    return OAuthLoginResponse(
        success=True,
        authorization_url=full_url,
        state=effective_state,
        nonce=effective_nonce,
        login_request=login_request,
    )


def start_login_flow(
    redirect_uri: str,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    connection: Optional[str] = None,
) -> OAuthLoginResponse:
    """
    High-level entry point to initiate an Auth0 authorization-code login.

    Provider: Auth0
    """
    response = build_authorization_url(
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
        connection=connection,
    )
    return response
