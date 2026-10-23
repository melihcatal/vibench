from __future__ import annotations

from identity_client import exchange_authorization_code, load_identity_config


def handle_oauth_callback(code: str) -> dict:
    config = load_identity_config()
    tokens = exchange_authorization_code(config, code)
    return tokens.raw
