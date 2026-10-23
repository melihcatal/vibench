import os
import secrets
import hashlib
import base64
import urllib.parse
from typing import Dict, Any, Tuple


def generate_pkce_verifier_and_challenge() -> Tuple[str, str, str]:
    """
    Generate PKCE code verifier and code challenge for public clients.
    Returns (code_verifier, code_challenge, code_challenge_method)
    """
    # Generate a random code verifier
    code_verifier = secrets.token_urlsafe(64)

    # Create SHA256 hash of the code verifier
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()

    # Base64 URL-safe encode the hash (without padding)
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode().replace("=", "")

    return code_verifier, code_challenge, "S256"


def start_auth0_pkce_login(
    redirect_uri: str, state: str = None, scope: str = "openid profile email"
) -> Tuple[str, str]:
    """
    Start PKCE OAuth/OIDC login flow with Auth0 for public clients.
    Returns (authorization_url, code_verifier)
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not auth0_domain or not client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set"
        )

    if state is None:
        state = secrets.token_urlsafe(32)

    code_verifier, code_challenge, challenge_method = (
        generate_pkce_verifier_and_challenge()
    )

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": challenge_method,
        "audience": f"https://{auth0_domain}/api/v2/",
    }

    auth_url = f"https://{auth0_domain}/authorize?{urllib.parse.urlencode(params)}"
    return auth_url, code_verifier


def exchange_auth0_pkce_code_for_tokens(
    authorization_code: str, code_verifier: str, redirect_uri: str
) -> Dict[str, Any]:
    """
    Exchange Auth0 authorization code for tokens using PKCE flow.
    """
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not auth0_domain or not client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set"
        )

    token_url = f"https://{auth0_domain}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": authorization_code,
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()

    return response.json()


def start_cognito_pkce_login(
    redirect_uri: str, state: str = None, scope: str = "openid profile email"
) -> Tuple[str, str]:
    """
    Start PKCE OAuth/OIDC login flow with Amazon Cognito for public clients.
    Returns (authorization_url, code_verifier)
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")

    if not cognito_domain or not client_id:
        raise ValueError(
            "COGNITO_DOMAIN and COGNITO_CLIENT_ID environment variables must be set"
        )

    if state is None:
        state = secrets.token_urlsafe(32)

    code_verifier, code_challenge, challenge_method = (
        generate_pkce_verifier_and_challenge()
    )

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": challenge_method,
    }

    auth_url = (
        f"https://{cognito_domain}/oauth2/authorize?{urllib.parse.urlencode(params)}"
    )
    return auth_url, code_verifier


def exchange_cognito_pkce_code_for_tokens(
    authorization_code: str, code_verifier: str, redirect_uri: str
) -> Dict[str, Any]:
    """
    Exchange Amazon Cognito authorization code for tokens using PKCE flow.
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")

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
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()
