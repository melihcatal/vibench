from __future__ import annotations

from typing import Dict
from urllib.parse import urlparse, parse_qs

from identity_client import discover_oidc_metadata, exchange_code_for_tokens, load_login_config

AUTH0_PROVIDER = "Auth0 Authentication API"


def handle_oauth_callback(callback_url: str) -> Dict[str, object]:
    config = load_login_config()
    metadata = discover_oidc_metadata(config.issuer)
    parsed = urlparse(callback_url)
    params = parse_qs(parsed.query)
    code = params.get("code", [None])[0]
    state = params.get("state", [None])[0]
    if not code:
        raise ValueError("authorization code missing")
    tokens = exchange_code_for_tokens(config, metadata, code=code)
    return {
        "provider": AUTH0_PROVIDER,
        "state": state,
        "tokens": tokens,
    }
