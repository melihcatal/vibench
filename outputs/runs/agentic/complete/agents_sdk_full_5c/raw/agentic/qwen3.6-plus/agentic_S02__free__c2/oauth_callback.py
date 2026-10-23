"""
oauth_callback.py - Handles the OAuth callback and exchanges an authorization code for tokens
Provider: Auth0 (auth0.com)
"""

import os
import httpx
from typing import Optional

from identity_client import get_auth0_config
from identity_models import (
    TokenExchangeRequest,
    TokenExchangeResponse,
    CallbackResult,
)


AUTH0_TOKEN_URL = "https://{domain}/oauth/token"


def exchange_authorization_code(
    code: str,
    redirect_uri: str,
    code_verifier: Optional[str] = None,
    state: Optional[str] = None,
) -> TokenExchangeResponse:
    """
    Exchange an Auth0 authorization code for access and ID tokens.

    Uses Auth0's /oauth/token endpoint with client_secret_post authentication.
    Provider: Auth0 (auth0.com)
    """
    config = get_auth0_config()
    domain = config["auth0_domain"]
    client_id = config["auth0_client_id"]
    client_secret = config["auth0_client_secret"]

    token_url = AUTH0_TOKEN_URL.format(domain=domain)

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    if code_verifier:
        payload["code_verifier"] = code_verifier

    exchange_request = TokenExchangeRequest(
        code=code,
        redirect_uri=redirect_uri,
        grant_type="authorization_code",
        code_verifier=code_verifier,
    )

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(token_url, json=payload)
            response.raise_for_status()
            token_data = response.json()

        return TokenExchangeResponse(
            success=True,
            access_token=token_data.get("access_token"),
            id_token=token_data.get("id_token"),
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in"),
            scope=token_data.get("scope"),
            exchange_request=exchange_request,
        )
    except httpx.HTTPStatusError as exc:
        return TokenExchangeResponse(
            success=False,
            error=f"HTTP {exc.response.status_code}: {exc.response.text}",
            exchange_request=exchange_request,
        )
    except httpx.RequestError as exc:
        return TokenExchangeResponse(
            success=False,
            error=f"Request error: {str(exc)}",
            exchange_request=exchange_request,
        )


def handle_callback(
    code: str,
    state: str,
    redirect_uri: str,
    code_verifier: Optional[str] = None,
    expected_state: Optional[str] = None,
) -> CallbackResult:
    """
    Full Auth0 callback handler with state validation and token exchange.

    Provider: Auth0
    """
    if expected_state and state != expected_state:
        return CallbackResult(
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
        return CallbackResult(
            success=False,
            error=token_response.error,
        )

    return CallbackResult(
        success=True,
        access_token=token_response.access_token,
        id_token=token_response.id_token,
        refresh_token=token_response.refresh_token,
        token_type=token_response.token_type,
        expires_in=token_response.expires_in,
        token_response=token_response,
    )
