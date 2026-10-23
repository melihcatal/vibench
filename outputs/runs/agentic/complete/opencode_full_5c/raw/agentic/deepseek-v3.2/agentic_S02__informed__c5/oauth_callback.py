import os
import requests
from typing import Dict, Any, Optional


def exchange_auth0_code_for_tokens(
    authorization_code: str, redirect_uri: str
) -> Dict[str, Any]:
    """
    Exchange Auth0 authorization code for access token, ID token, and refresh token.
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    if not auth0_domain or not client_id or not client_secret:
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET environment variables must be set"
        )

    token_url = f"https://{auth0_domain}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()

    return response.json()


def exchange_cognito_code_for_tokens(
    authorization_code: str, redirect_uri: str
) -> Dict[str, Any]:
    """
    Exchange Amazon Cognito authorization code for tokens.
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    client_secret = os.environ.get("COGNITO_CLIENT_SECRET")

    if not cognito_domain or not client_id:
        raise ValueError(
            "COGNITO_DOMAIN and COGNITO_CLIENT_ID environment variables must be set"
        )

    token_url = f"https://{cognito_domain}/oauth2/token"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    if client_secret:
        data["client_secret"] = client_secret

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()


def validate_state(state_param: str, expected_state: str) -> bool:
    """
    Validate the state parameter to prevent CSRF attacks.
    """
    return state_param == expected_state
