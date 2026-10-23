from __future__ import annotations

import secrets

from identity_client import auth0_authorize_url, load_identity_config
from identity_models import LoginRequest


def build_start_url() -> str:
    cfg = load_identity_config()
    req = LoginRequest(
        issuer=cfg["issuer"],
        client_id=cfg["client_id"],
        redirect_uri=cfg["redirect_uri"],
        state=secrets.token_urlsafe(16),
        nonce=secrets.token_urlsafe(16),
    )
    return auth0_authorize_url(req)
