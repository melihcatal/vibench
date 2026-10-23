"""
pkce_login.py - Implements a PKCE (Proof Key for Code Exchange) login flow for public clients
Provider: Auth0 (auth0.com)
"""

import os
import secrets
import hashlib
import base64
import urllib.parse
from typing import Optional

from identity_client import get_auth0_config
from identity_models import (
    PKCELoginRequest,
    PKCELoginResponse,
    PKCECallbackResult,
)
from oauth_callback import exchange_authorization_code


AUTH0_AUTHORIZE_URL = "https://{domain}/authorize"


def base64url_encode(data: bytes) -> str:
    """Base64url encode bytes without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_code_verifier() -> str:
    """Generate a PKCE code_verifier (43-128 characters)."""
    return secrets.token_urlsafe(48)


def generate_code_challenge(code_verifier: str) -> str:
    """
    Generate a PKCE code_challenge using S256 method.

    code_challenge = BASE64URL(SHA256(ASCII(code_verifier)))
    """
    sha256_hash = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64url_encode(sha256_hash)


def build_pkce_authorization_url(
    redirect_uri: str,
    code_verifier: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    state: Optional[str] = None,
    connection: Optional[str] = None,
) -> PKCELoginResponse:
    """
    Build an Auth0 authorization URL with PKCE parameters.

    Uses Auth0's OIDC /authorize endpoint with code_challenge and code_challenge_method=S256.
    Provider: Auth0 (auth0.com)
    """
    config = get_auth0_config()
    domain = config["auth0_domain"]
    client_id = config["auth0_client_id"]

    verifier = code_verifier or generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    effective_state = state or secrets.token_urlsafe(32)
    effective_scope = scope or "openid profile email"

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": effective_scope,
        "state": effective_state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    if audience:
        params["audience"] = audience
    if connection:
        params["connection"] = connection

    authorize_url = AUTH0_AUTHORIZE_URL.format(domain=domain)
    full_url = f"{authorize_url}?{urllib.parse.urlencode(params)}"

    login_request = PKCELoginRequest(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=effective_scope,
        state=effective_state,
        code_verifier=verifier,
        code_challenge=challenge,
        code_challenge_method="S256",
        audience=audience,
        connection=connection,
        authorize_url=full_url,
    )

    return PKCELoginResponse(
        success=True,
        authorization_url=full_url,
        state=effective_state,
        code_verifier=verifier,
        code_challenge=challenge,
        login_request=login_request,
    )


def handle_pkce_callback(
    code: str,
    state: str,
    redirect_uri: str,
    code_verifier: str,
    expected_state: Optional[str] = None,
) -> PKCECallbackResult:
    """
    Handle Auth0 PKCE callback with code_verifier exchange.

    Provider: Auth0
    """
    if expected_state and state != expected_state:
        return PKCECallbackResult(
            success=False,
            error="State mismatch: possible CSRF attack",
        )

    token_response = exchange_authorization_code(
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
        state=state,
    )

    if not token_response.success:
        return PKCECallbackResult(
            success=False,
            error=token_response.error,
        )

    return PKCECallbackResult(
        success=True,
        access_token=token_response.access_token,
        id_token=token_response.id_token,
        refresh_token=token_response.refresh_token,
        token_type=token_response.token_type,
        expires_in=token_response.expires_in,
        code_verifier=code_verifier,
        token_response=token_response,
    )
