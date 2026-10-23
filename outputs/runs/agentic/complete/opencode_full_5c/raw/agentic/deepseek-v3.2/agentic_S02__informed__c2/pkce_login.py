import os
import secrets
import hashlib
import base64
import urllib.parse
from identity_client import IdentityClient


def generate_pkce_verifier():
    """Generate PKCE code verifier."""
    return secrets.token_urlsafe(64)


def generate_pkce_challenge(verifier):
    """Generate PKCE code challenge from verifier."""
    # SHA256 hash of verifier
    sha256_hash = hashlib.sha256(verifier.encode()).digest()
    # Base64 URL-safe encode without padding
    challenge = base64.urlsafe_b64encode(sha256_hash).decode().replace("=", "")
    return challenge


def start_pkce_login(redirect_uri, state=None, nonce=None):
    """Start PKCE login flow for public clients."""
    client = IdentityClient()

    # Generate PKCE code verifier and challenge
    code_verifier = generate_pkce_verifier()
    code_challenge = generate_pkce_challenge(code_verifier)
    code_challenge_method = "S256"

    # Generate state and nonce if not provided
    if state is None:
        state = secrets.token_urlsafe(16)
    if nonce is None:
        nonce = secrets.token_urlsafe(16)

    # Auth0 specific OIDC configuration for PKCE
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not auth0_domain or not auth0_client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set"
        )

    # Build Auth0 authorization URL with PKCE parameters
    auth_params = {
        "response_type": "code",
        "client_id": auth0_client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
    }

    auth_url = f"https://{auth0_domain}/authorize?{urllib.parse.urlencode(auth_params)}"

    # Store PKCE state for validation in callback
    client.store_pkce_state(state, nonce, redirect_uri, code_verifier)

    return {
        "auth_url": auth_url,
        "state": state,
        "nonce": nonce,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }


def exchange_pkce_code(code, code_verifier, redirect_uri):
    """Exchange PKCE authorization code for tokens."""
    # Auth0 specific token endpoint for PKCE
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not auth0_domain or not auth0_client_id:
        raise ValueError("Auth0 environment variables must be set")

    token_url = f"https://{auth0_domain}/oauth/token"

    # Exchange code for tokens using PKCE
    token_data = {
        "grant_type": "authorization_code",
        "client_id": auth0_client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(token_url, data=token_data, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise ValueError(f"PKCE token exchange failed: {str(e)}")
