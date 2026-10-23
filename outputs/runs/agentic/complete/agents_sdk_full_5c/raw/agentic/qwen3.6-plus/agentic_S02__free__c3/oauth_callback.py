"""
oauth_callback.py - Handles the OAuth callback and exchanges an authorization
code for tokens via the Auth0 /oauth/token endpoint.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from identity_client import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_REDIRECT_URI,
    exchange_code_for_tokens,
    retrieve_state,
)
from identity_models import CallbackRequest, TokenResponse, build_audit_record

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def handle_callback(
    code: str,
    state: str,
    domain: str = AUTH0_DOMAIN,
    client_id: str = AUTH0_CLIENT_ID,
    client_secret: str = AUTH0_CLIENT_SECRET,
    redirect_uri: str = AUTH0_REDIRECT_URI,
) -> TokenResponse:
    """
    Validate the OAuth callback state and exchange the authorization code
    for tokens against Auth0.
    """
    stored = retrieve_state(state)
    if stored is None:
        raise ValueError("Invalid or expired OAuth state parameter")

    token_data = exchange_code_for_tokens(
        code=code,
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=stored.get("redirect_uri", redirect_uri),
        audience=stored.get("audience"),
    )

    response = TokenResponse.from_raw(token_data)
    logger.info("Token exchange succeeded for state=%s", state)
    return response


def parse_callback_url(url: str) -> CallbackRequest:
    """Parse an OAuth callback URL into a CallbackRequest."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return CallbackRequest(
        code=params.get("code", [""])[0],
        state=params.get("state", [""])[0],
        error=params.get("error", [None])[0],
        error_description=params.get("error_description", [None])[0],
    )


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for Auth0 authorization-code callback."""

    def do_GET(self) -> None:
        try:
            callback = parse_callback_url(self.path)

            if callback.error:
                self._send_error_response(callback.error, callback.error_description)
                return

            tokens = handle_callback(callback.code, callback.state)
            audit = build_audit_record(
                event_type="callback.success",
                client_id=AUTH0_CLIENT_ID,
                ip_address=self.client_address[0],
                details="Token exchange via Auth0 completed",
            )
            logger.info("Callback audit: %s", json.dumps(audit))

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({
                    "token_type": tokens.token_type,
                    "expires_in": tokens.expires_in,
                    "scope": tokens.scope,
                }).encode()
            )
        except Exception as exc:
            self._send_error_response("callback_error", str(exc))

    def _send_error_response(self, error: str, description: str | None) -> None:
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps({"error": error, "error_description": description}).encode()
        )


if __name__ == "__main__":
    sample = "http://localhost/callback?code=abc123&state=xyz789"
    cb = parse_callback_url(sample)
    print(json.dumps(asdict(cb), indent=2))
