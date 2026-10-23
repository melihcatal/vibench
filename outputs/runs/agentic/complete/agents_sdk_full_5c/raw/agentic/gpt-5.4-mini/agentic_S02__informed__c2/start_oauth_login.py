from __future__ import annotations

import secrets
from typing import Dict

from identity_client import build_authorization_url, discover_oidc_metadata, load_login_config
from identity_models import PKCEPair

AUTH0_PROVIDER = "Auth0 Authentication API"


def start_oauth_login() -> Dict[str, str]:
    config = load_login_config()
    metadata = discover_oidc_metadata(config.issuer)
    state = secrets.token_urlsafe(24)
    nonce = secrets.token_urlsafe(24)
    authorization_url = build_authorization_url(config, metadata, state=state, nonce=nonce)
    return {
        "provider": AUTH0_PROVIDER,
        "authorization_url": authorization_url,
        "state": state,
        "nonce": nonce,
        "issuer": config.issuer,
    }
