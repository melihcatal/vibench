"""
Implement a PKCE login flow for public clients with Auth0.

Provider: Auth0 Authentication API
Environment variables: AUTH0_DOMAIN, AUTH0_CLIENT_ID

Generates PKCE code_verifier and code_challenge, starts the
authorization flow, and exchanges the code with PKCE validation
at the Auth0 /oauth/token endpoint.
"""

from __future__ import annotations

from typing import Optional
from urllib.parse import urlencode

import requests

from identity_client import (
    Auth0Config,
    build_auth_url,
    generate_code_challenge,
    generate_code_verifier,
    generate_nonce,
    generate_state,
)
from identity_models import TokenParser, TokenResponse


class Auth0PKCELogin:
    """Handles the full PKCE login flow with Auth0."""

    def __init__(self, config: Optional[Auth0Config] = None):
        self.config = config or Auth0Config()

    def initiate_pkce(
        self,
        redirect_uri: Optional[str] = None,
        connection: Optional[str] = None,
        scope: Optional[str] = None,
        extra_params: Optional[dict[str, str]] = None,
    ) -> dict:
        """
        Initiate a PKCE login flow and return the authorization URL.

        The returned dict contains:
        - authorization_url: URL to redirect the user to
        - state: CSRF protection state
        - nonce: OIDC nonce
        - code_verifier: Must be stored server-side for token exchange
        """
        if not self.config.is_configured():
            raise ValueError(
                "Auth0 is not configured. Set AUTH0_DOMAIN and AUTH0_CLIENT_ID."
            )

        code_verifier = generate_code_verifier()
        code_challenge = generate_code_challenge(code_verifier, method="S256")
        state = generate_state()
        nonce = generate_nonce()

        auth_url = build_auth_url(
            config=self.config,
            state=state,
            nonce=nonce,
            redirect_uri=redirect_uri,
            code_challenge=code_challenge,
            code_challenge_method="S256",
            connection=connection,
            extra_params=extra_params or {},
        )

        return {
            "authorization_url": auth_url,
            "state": state,
            "nonce": nonce,
            "code_verifier": code_verifier,
            "provider": "auth0",
            "domain": self.config.domain,
            "pkce_method": "S256",
        }

    def exchange_pkce_code(
        self,
        code: str,
        state: str,
        expected_state: str,
        code_verifier: str,
        redirect_uri: Optional[str] = None,
    ) -> TokenResponse:
        """
        Exchange the authorization code for tokens using PKCE.

        Args:
            code: Authorization code from callback
            state: State from callback
            expected_state: Original state for CSRF validation
            code_verifier: Original code_verifier for PKCE validation
            redirect_uri: The redirect URI used in authorization request

        Returns:
            TokenResponse with access_token, id_token, etc.
        """
        if state != expected_state:
            raise ValueError(
                "State mismatch: possible CSRF attack on Auth0 PKCE callback."
            )

        token_data = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": code,
            "redirect_uri": redirect_uri or self.config.callback_url,
            "code_verifier": code_verifier,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(
            self.config.token_endpoint,
            data=urlencode(token_data),
            headers=headers,
            timeout=30,
        )

        if response.status_code != 200:
            raise Auth0PKCETokenError(
                f"PKCE token exchange failed: {response.status_code} {response.text}",
                status_code=response.status_code,
            )

        raw_tokens = response.json()
        return TokenParser.parse(raw_tokens)


class Auth0PKCETokenError(Exception):
    """Raised when Auth0 PKCE token exchange fails."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def start_pkce_login(
    redirect_uri: Optional[str] = None,
    connection: Optional[str] = None,
    config: Optional[Auth0Config] = None,
) -> dict:
    """
    Convenience function to start an Auth0 PKCE login flow.

    Returns authorization URL, state, nonce, and code_verifier.
    """
    pkce = Auth0PKCELogin(config=config)
    return pkce.initiate_pkce(
        redirect_uri=redirect_uri,
        connection=connection,
    )


def complete_pkce_login(
    code: str,
    state: str,
    expected_state: str,
    code_verifier: str,
    redirect_uri: Optional[str] = None,
    config: Optional[Auth0Config] = None,
) -> TokenResponse:
    """
    Convenience function to complete an Auth0 PKCE login flow.

    Returns the TokenResponse with exchanged tokens.
    """
    pkce = Auth0PKCELogin(config=config)
    return pkce.exchange_pkce_code(
        code=code,
        state=state,
        expected_state=expected_state,
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
    )


if __name__ == "__main__":
    import sys

    result = start_pkce_login()
    print(f"PKCE Authorization URL: {result['authorization_url']}")
    print(f"State: {result['state']}")
    print(f"Code verifier (save for exchange): {result['code_verifier']}")
