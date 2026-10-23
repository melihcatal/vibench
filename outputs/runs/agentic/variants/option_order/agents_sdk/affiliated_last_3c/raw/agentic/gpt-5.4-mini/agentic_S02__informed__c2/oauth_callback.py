from __future__ import annotations

from identity_client import Auth0IdentityClient


def handle_oauth_callback(code: str, redirect_uri: str | None = None, code_verifier: str | None = None):
    client = Auth0IdentityClient()
    return client.exchange_code(code=code, redirect_uri=redirect_uri, code_verifier=code_verifier)
