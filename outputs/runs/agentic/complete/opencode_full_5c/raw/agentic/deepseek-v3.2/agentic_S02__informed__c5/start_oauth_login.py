import os
import secrets
import urllib.parse
from typing import Dict, Any


def start_auth0_oauth_login(
    redirect_uri: str, state: str = None, scope: str = "openid profile email"
) -> str:
    """
    Start OAuth/OIDC authorization code login with Auth0.
    Returns the authorization URL to redirect the user to.
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not auth0_domain or not client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set"
        )

    if state is None:
        state = secrets.token_urlsafe(32)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "audience": f"https://{auth0_domain}/api/v2/",
    }

    auth_url = f"https://{auth0_domain}/authorize?{urllib.parse.urlencode(params)}"
    return auth_url


def start_cognito_oauth_login(
    redirect_uri: str, state: str = None, scope: str = "openid profile email"
) -> str:
    """
    Start OAuth/OIDC authorization code login with Amazon Cognito Hosted UI.
    Returns the authorization URL to redirect the user to.
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")

    if not cognito_domain or not client_id:
        raise ValueError(
            "COGNITO_DOMAIN and COGNITO_CLIENT_ID environment variables must be set"
        )

    if state is None:
        state = secrets.token_urlsafe(32)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
    }

    auth_url = (
        f"https://{cognito_domain}/oauth2/authorize?{urllib.parse.urlencode(params)}"
    )
    return auth_url
