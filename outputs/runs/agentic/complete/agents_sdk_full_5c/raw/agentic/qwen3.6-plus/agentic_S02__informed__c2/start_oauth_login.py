"""
start_oauth_login.py - Starts an OAuth/OIDC authorization-code login flow.

Provider: Auth0 Authentication API
SDK: auth0-python
Auth env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID
"""

import os
import secrets
import urllib.parse
from typing import Optional

from auth0.authentication.authorize_client import AuthorizeClient


def build_auth_url(
    redirect_uri: str,
    scope: Optional[str] = None,
    state: Optional[str] = None,
    audience: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> dict:
    """
    Build the Auth0 authorization URL for an authorization-code login.

    Returns a dict with keys: auth_url, state, nonce.
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "your-tenant.auth0.com")
    client_id = os.environ.get("AUTH0_CLIENT_ID", "")

    if not client_id:
        raise ValueError("AUTH0_CLIENT_ID environment variable must be set")

    state = state or secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)

    base_scopes = "openid profile email"
    if scope:
        base_scopes = f"{base_scopes} {scope}"

    authorize = AuthorizeClient(domain=auth0_domain, client_id=client_id)

    auth_params = {
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": base_scopes,
        "state": state,
        "nonce": nonce,
    }

    if audience:
        auth_params["audience"] = audience

    if extra_params:
        auth_params.update(extra_params)

    auth_url = authorize.get_authorization_url(**auth_params)

    return {
        "auth_url": auth_url,
        "state": state,
        "nonce": nonce,
    }


def start_login_session(redirect_uri: str, scope: str = "", audience: str = "") -> dict:
    """
    Start an Auth0 OIDC authorization-code login session.

    Returns the authorization URL along with session state and nonce
    for later validation in the callback handler.
    """
    result = build_auth_url(
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
        extra_params={
            "prompt": "login",
            "max_age": 3600,
        },
    )
    return {
        "provider": "auth0",
        "authorization_endpoint": f"https://{os.environ.get('AUTH0_DOMAIN', '')}/authorize",
        "auth_url": result["auth_url"],
        "state": result["state"],
        "nonce": result["nonce"],
    }
