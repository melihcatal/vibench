from __future__ import annotations

import secrets
from typing import Dict

from identity_client import build_authorization_url, create_pkce_pair, discover_oidc_metadata, load_login_config

AUTH0_PROVIDER = "Auth0 Authentication API"


def start_pkce_login() -> Dict[str, str]:
    config = load_login_config()
    metadata = discover_oidc_metadata(config.issuer)
    pkce = create_pkce_pair()
    state = secrets.token_urlsafe(24)
    nonce = secrets.token_urlsafe(24)
    authorization_url = build_authorization_url(config, metadata, state=state, nonce=nonce, pkce=pkce)
    return {
        "provider": AUTH0_PROVIDER,
        "authorization_url": authorization_url,
        "state": state,
        "nonce": nonce,
        "code_verifier": pkce.code_verifier,
        "code_challenge": pkce.code_challenge,
        "code_challenge_method": pkce.method,
    }
