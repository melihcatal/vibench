from __future__ import annotations

from identity_client import build_authorize_url, load_identity_config
from identity_models import LoginRequest


def start_oauth_login(state: str, nonce: str, redirect_uri: str = "") -> str:
    config = load_identity_config("AUTH0")
    req = LoginRequest(
        redirect_uri=redirect_uri or config.redirect_uri,
        state=state,
        nonce=nonce,
    )
    return build_authorize_url(config, req)
