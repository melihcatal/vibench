"""
Start an OAuth or OIDC authorization-code login flow with Auth0.
Constructs the authorization URL and redirects the user to the Auth0 /authorize endpoint.
"""

import os
import uuid
from typing import Optional, Dict, Any

from identity_client import (
    create_auth0_client,
    generate_state,
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
    AUTH0_AUDIENCE,
)
from identity_models import validate_redirect_uri


def start_oauth_login(
    scope: str = "openid profile email",
    redirect_uri: Optional[str] = None,
    audience: Optional[str] = None,
    connection: Optional[str] = None,
    prompt: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
    state: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Initiate an Auth0 authorization-code login flow.

    Returns a dict with the authorization URL and state for session tracking.
    """
    client = create_auth0_client(
        domain=os.getenv("AUTH0_DOMAIN", AUTH0_DOMAIN),
        client_id=os.getenv("AUTH0_CLIENT_ID", AUTH0_CLIENT_ID),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET", ""),
        redirect_uri=redirect_uri or os.getenv("AUTH0_REDIRECT_URI", AUTH0_REDIRECT_URI),
        audience=audience or os.getenv("AUTH0_AUDIENCE", AUTH0_AUDIENCE),
    )

    if redirect_uri and not validate_redirect_uri(redirect_uri):
        raise ValueError(f"Invalid redirect URI: {redirect_uri}")

    login_state = state or generate_state()

    params = extra_params or {}
    if connection:
        params["connection"] = connection
    if prompt:
        params["prompt"] = prompt

    auth_url = client.authorize_url(
        state=login_state,
        scope=scope,
        response_type="code",
        extra_params=params,
    )

    session_data = {
        "state": login_state,
        "nonce": uuid.uuid4().hex,
        "redirect_uri": redirect_uri or client.redirect_uri,
        "scope": scope,
        "auth0_domain": client.domain,
        "auth0_client_id": client.client_id,
    }

    return {
        "authorization_url": auth_url,
        "state": login_state,
        "session_data": session_data,
    }


def build_login_redirect(
    response: Dict[str, Any],
    redirect_status_code: int = 302,
) -> Dict[str, Any]:
    """
    Build an HTTP redirect response for the authorization URL.
    Suitable for web framework integration (Flask, FastAPI, etc.).
    """
    return {
        "status_code": redirect_status_code,
        "headers": {
            "Location": response["authorization_url"],
        },
        "session": response["session_data"],
    }


if __name__ == "__main__":
    result = start_oauth_login()
    print(f"Authorization URL: {result['authorization_url']}")
    print(f"State: {result['state']}")
