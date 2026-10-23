from __future__ import annotations

from identity_client import exchange_code, load_auth0_config
from identity_models import TokenExchangeRequest, TokenSet


def handle_oauth_callback(code: str, code_verifier: str = "") -> TokenSet:
    cfg = load_auth0_config()
    req = TokenExchangeRequest(
        issuer=cfg["issuer"],
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        code=code,
        redirect_uri=cfg["redirect_uri"],
        code_verifier=code_verifier,
    )
    return exchange_code(req)
