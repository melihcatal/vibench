"""Local configuration and client helper utilities for Federated Login Flow.

This module provides configuration loading, HTTP session management,
and reusable helpers for interacting with Auth0 as the OAuth/OIDC provider.
"""

import os
from typing import Any, Dict, Optional
import secrets
import hashlib
import base64

# Auth0 provider identifiers
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8080/callback")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")
AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")

# Auth0 endpoint constants (provider-specific hostnames)
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}" if AUTH0_DOMAIN else None
AUTH0_AUTHORIZATION_ENDPOINT = f"{AUTH0_ISSUER}/authorize" if AUTH0_ISSUER else None
AUTH0_TOKEN_ENDPOINT = f"{AUTH0_ISSUER}/oauth/token" if AUTH0_ISSUER else None
AUTH0_USERINFO_ENDPOINT = f"{AUTH0_ISSUER}/userinfo" if AUTH0_ISSUER else None
AUTH0_OIDC_DISCOVERY = f"{AUTH0_ISSUER}/.well-known/openid-configuration" if AUTH0_ISSUER else None


def generate_state() -> str:
    """Generate a cryptographically secure state parameter."""
    return secrets.token_urlsafe(32)


def generate_code_verifier() -> str:
    """Generate a PKCE code verifier (43-128 URL-safe characters)."""
    return secrets.token_urlsafe(64)


def generate_code_challenge(verifier: str) -> str:
    """Generate a PKCE code challenge from a code verifier using S256 method."""
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_authorization_url(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    state: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: str = "S256",
    audience: Optional[str] = None,
    response_type: str = "code",
) -> str:
    """Build the Auth0 authorization URL with query parameters."""
    if not AUTH0_AUTHORIZATION_ENDPOINT:
        raise ValueError("AUTH0_DOMAIN environment variable is not set")

    params: Dict[str, str] = {
        "client_id": client_id or AUTH0_CLIENT_ID or "",
        "redirect_uri": redirect_uri or AUTH0_CALLBACK_URL,
        "scope": scope or AUTH0_SCOPE,
        "state": state or generate_state(),
        "response_type": response_type,
    }

    if audience or AUTH0_AUDIENCE:
        params["audience"] = audience or AUTH0_AUDIENCE

    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = code_challenge_method

    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{AUTH0_AUTHORIZATION_ENDPOINT}?{query_string}"


def validate_state(received_state: str, expected_state: str) -> bool:
    """Validate the OAuth state parameter to prevent CSRF attacks."""
    if not received_state or not expected_state:
        return False
    return secrets.compare_digest(received_state, expected_state)


def parse_id_token_claims(id_token: str) -> Dict[str, Any]:
    """Decode JWT ID token payload without verification (for inspection only)."""
    parts = id_token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT token format")
    payload = parts[1]
    padded = payload + "=" * (4 - len(payload) % 4)
    decoded = base64.urlsafe_b64decode(padded)
    import json
    return json.loads(decoded)
