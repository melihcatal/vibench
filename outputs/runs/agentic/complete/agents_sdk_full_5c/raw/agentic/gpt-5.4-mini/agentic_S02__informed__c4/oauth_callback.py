from __future__ import annotations

from identity_client import exchange_auth0_code, load_identity_config
from identity_models import TokenResponse


def handle_callback(code: str) -> TokenResponse:
    cfg = load_identity_config()
    return exchange_auth0_code(cfg["issuer"], cfg["client_id"], cfg["client_secret"], code, cfg["redirect_uri"])
