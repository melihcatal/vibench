import os
import hashlib
import base64
from urllib.parse import urlencode

from identity_client import get_auth0_domain, get_auth0_client_id


def generate_pkce_challenge(code_verifier: str) -> str:
    """Generates a PKCE code challenge from a code verifier."""
    sha256_hash = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    # urlsafe_b64encode also handles padding removal
    return base64.urlsafe_b64encode(sha256_hash).decode("utf-8").replace("=", "")


def start_pkce_login(code_verifier: str) -> str:
    """Implements a PKCE login flow for public clients with Auth0.
    Returns the authorization URL.
    """
    auth0_domain = get_auth0_domain()
    auth0_client_id = get_auth0_client_id()
    redirect_uri = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )
    audience = os.environ.get("AUTH0_AUDIENCE", f"https://{auth0_domain}/api/v2/")

    code_challenge = generate_pkce_challenge(code_verifier)
    code_challenge_method = "S256"

    auth_url = (
        f"https://{auth0_domain}/authorize?"
        + urlencode(
            {
                "response_type": "code",
                "client_id": auth0_client_id,
                "redirect_uri": redirect_uri,
                "audience": audience,
                "scope": "openid profile email",
                "code_challenge": code_challenge,
                "code_challenge_method": code_challenge_method,
                "state": "some_random_pkce_state",  # In a real app, generate a unique state and verify it in the callback
            }
        )
    )
    return auth_url


def exchange_pkce_code_for_tokens(authorization_code: str, code_verifier: str) -> dict:
    """Exchanges the authorization code for tokens using PKCE with Auth0."""
    import requests

    auth0_domain = get_auth0_domain()
    auth0_client_id = get_auth0_client_id()
    redirect_uri = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )

    token_url = f"https://{auth0_domain}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": auth0_client_id,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
