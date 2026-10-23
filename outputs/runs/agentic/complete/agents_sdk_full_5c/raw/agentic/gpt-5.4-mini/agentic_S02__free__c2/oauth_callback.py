from __future__ import annotations

from identity_client import IdentityClient

AUTH0_STYLE_CALLBACK = "oauth2/callback"


def oauth_callback(code: str) -> dict:
    client = IdentityClient()
    tokens = client.exchange_code(code)
    return tokens.raw
