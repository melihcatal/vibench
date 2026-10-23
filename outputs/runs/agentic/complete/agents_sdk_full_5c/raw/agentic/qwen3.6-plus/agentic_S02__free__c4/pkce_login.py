"""
Implement PKCE (Proof Key for Code Exchange) login flow for public clients using Auth0.

Provider: Auth0 Authentication API (https://auth0.com/docs/api/authentication)
"""

import os
import base64
import hashlib
import secrets
import time
import json
from typing import Optional

import requests
from identity_client import get_pkce_config


# Auth0 configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "dev-example.us.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "abc123def456ghi789")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "https://app.example.com/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "https://api.example.com")

# Auth0 endpoints
AUTH0_AUTHORIZE_URL = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"

PKCE_CODE_VERIFIER_LENGTH = 64


def generate_code_verifier(length: int = PKCE_CODE_VERIFIER_LENGTH) -> str:
    """Generate PKCE code_verifier (cryptographically random string)."""
    return secrets.token_urlsafe(length)[:length]


def generate_code_challenge(code_verifier: str) -> str:
    """
    Generate PKCE code_challenge from code_verifier using SHA-256.

    Per RFC 7636: code_challenge = BASE64URL(SHA256(code_verifier))
    """
    sha256_hash = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(sha256_hash).rstrip(b"=").decode("ascii")


def build_pkce_authorization_url(
    code_challenge: str,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> str:
    """
    Build Auth0 authorization URL with PKCE parameters.

    Uses code_challenge_method=S256 per Auth0 requirements for PKCE.
    """
    from urllib.parse import urlencode

    if state is None:
        state = secrets.token_urlsafe(32)
    if nonce is None:
        nonce = secrets.token_urlsafe(32)

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
        "nonce": nonce,
        "scope": "openid profile email",
    }

    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE

    if extra_params:
        params.update(extra_params)

    query_string = urlencode(params)
    return f"{AUTH0_AUTHORIZE_URL}?{query_string}", state, nonce


def exchange_pkce_code(
    authorization_code: str,
    code_verifier: str,
    received_state: Optional[str] = None,
    expected_state: Optional[str] = None,
) -> dict:
    """
    Exchange Auth0 authorization code for tokens using PKCE.

    Calls Auth0 /oauth/token endpoint with code_verifier instead of client_secret.
    """
    if expected_state and received_state:
        import hmac
        if not hmac.compare_digest(received_state, expected_state):
            raise ValueError("State parameter mismatch - possible CSRF attack")

    token_payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": authorization_code,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        AUTH0_TOKEN_URL,
        json=token_payload,
        headers=headers,
        timeout=30,
    )

    if response.status_code != 200:
        raise Auth0PKCEError(
            f"Auth0 token exchange failed: {response.status_code} - {response.text}"
        )

    return response.json()


class Auth0PKCEError(Exception):
    """Raised when Auth0 PKCE flow fails."""
    pass


def start_pkce_login_flow(session_id: Optional[str] = None) -> dict:
    """
    Start the complete Auth0 PKCE login flow.

    Returns authorization URL, code_verifier, state, and nonce.
    The code_verifier must be stored server-side until callback.
    """
    import uuid
    if session_id is None:
        session_id = str(uuid.uuid4())

    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    auth_url, state, nonce = build_pkce_authorization_url(code_challenge)

    return {
        "session_id": session_id,
        "authorization_url": auth_url,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "state": state,
        "nonce": nonce,
        "provider": "auth0",
        "flow_type": "pkce",
    }


def complete_pkce_login(
    authorization_code: str,
    code_verifier: str,
    state: str,
    nonce: str,
) -> dict:
    """
    Complete the Auth0 PKCE login by exchanging code and fetching userinfo.
    """
    token_response = exchange_pkce_code(
        authorization_code=authorization_code,
        code_verifier=code_verifier,
        received_state=state,
        expected_state=state,
    )

    access_token = token_response.get("access_token")
    user_info = {}
    if access_token:
        userinfo_response = requests.get(
            AUTH0_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15,
        )
        if userinfo_response.status_code == 200:
            user_info = userinfo_response.json()

    return {
        "access_token": access_token,
        "id_token": token_response.get("id_token"),
        "refresh_token": token_response.get("refresh_token"),
        "expires_in": token_response.get("expires_in"),
        "token_type": token_response.get("token_type", "Bearer"),
        "user_info": user_info,
        "provider": "auth0",
        "flow_type": "pkce",
        "authenticated_at": int(time.time()),
    }


if __name__ == "__main__":
    flow = start_pkce_login_flow()
    print(json.dumps({
        "session_id": flow["session_id"],
        "authorization_url": flow["authorization_url"],
        "provider": flow["provider"],
        "flow_type": flow["flow_type"],
    }, indent=2))
