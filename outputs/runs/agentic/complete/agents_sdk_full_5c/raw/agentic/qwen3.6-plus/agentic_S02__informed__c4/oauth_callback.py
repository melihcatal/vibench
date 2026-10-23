"""
Handle the OAuth callback and exchange an authorization code for tokens.

Provider: Auth0 Authentication API
Environment variables: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET

Validates the state parameter and exchanges the authorization code
for access and ID tokens via the Auth0 /oauth/token endpoint.
"""

from __future__ import annotations

import base64
import json
from typing import Optional
from urllib.parse import urlencode

import requests

from identity_client import Auth0Config
from identity_models import CallbackRequest, TokenParser, TokenResponse


class Auth0CallbackHandler:
    """Handles Auth0 OAuth callback and token exchange."""

    def __init__(self, config: Optional[Auth0Config] = None):
        self.config = config or Auth0Config()

    def handle_callback(
        self,
        code: str,
        state: str,
        expected_state: str,
        redirect_uri: Optional[str] = None,
        code_verifier: Optional[str] = None,
    ) -> TokenResponse:
        """
        Process an Auth0 callback and exchange the authorization code for tokens.

        Args:
            code: The authorization code from the callback query string
            state: The state returned in the callback
            expected_state: The state that was stored when starting login
            redirect_uri: The redirect URI used in the authorization request
            code_verifier: The PKCE code_verifier if using PKCE flow

        Returns:
            TokenResponse with access_token, id_token, etc.
        """
        if state != expected_state:
            raise ValueError(
                "State mismatch: possible CSRF attack on Auth0 callback."
            )

        callback_request = CallbackRequest(
            code=code,
            state=state,
            expected_state=expected_state,
            redirect_uri=redirect_uri or self.config.callback_url,
            code_verifier=code_verifier,
        )

        return self._exchange_code(callback_request)

    def _exchange_code(self, request: CallbackRequest) -> TokenResponse:
        """Exchange authorization code for tokens at Auth0 /oauth/token."""
        token_data = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "code": request.code,
            "redirect_uri": request.redirect_uri,
        }

        if request.code_verifier:
            token_data["code_verifier"] = request.code_verifier

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            self.config.token_endpoint,
            data=urlencode(token_data),
            headers=headers,
            timeout=30,
        )

        if response.status_code != 200:
            raise Auth0TokenExchangeError(
                f"Token exchange failed: {response.status_code} {response.text}",
                status_code=response.status_code,
            )

        raw_tokens = response.json()
        return TokenParser.parse(raw_tokens)

    def validate_id_token(self, id_token: str) -> dict:
        """
        Decode and validate the ID token header and payload.

        Note: Full validation requires fetching JWKS from Auth0 and
        verifying the signature. This method performs basic decoding.
        """
        parts = id_token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT format for Auth0 ID token.")

        payload = parts[1]
        padded = payload + "=" * (4 - len(payload) % 4)
        decoded = base64.urlsafe_b64decode(padded)
        return json.loads(decoded)


class Auth0TokenExchangeError(Exception):
    """Raised when Auth0 token exchange fails."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def handle_oauth_callback(
    code: str,
    state: str,
    expected_state: str,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
    config: Optional[Auth0Config] = None,
) -> TokenResponse:
    """
    Convenience function to handle an Auth0 OAuth callback.

    Returns a TokenResponse with the exchanged tokens.
    """
    handler = Auth0CallbackHandler(config=config)
    return handler.handle_callback(
        code=code,
        state=state,
        expected_state=expected_state,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python oauth_callback.py <code> <state> [expected_state]")
        sys.exit(1)

    code = sys.argv[1]
    state = sys.argv[2]
    expected = sys.argv[3] if len(sys.argv) > 3 else state

    try:
        tokens = handle_oauth_callback(code=code, state=state, expected_state=expected)
        print(f"Access token: {tokens.access_token[:20]}...")
        if tokens.id_token:
            print(f"ID token: {tokens.id_token[:20]}...")
    except Auth0TokenExchangeError as e:
        print(f"Error: {e}")
