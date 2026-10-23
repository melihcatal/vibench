from __future__ import annotations

from identity_client import auth0_authorize_url, load_auth0_config
from identity_models import AuthorizationRequest


def build_start_login_url(state: str, nonce: str) -> str:
    cfg = load_auth0_config()
    req = AuthorizationRequest(
        issuer=cfg["issuer"],
        client_id=cfg["client_id"],
        redirect_uri=cfg["redirect_uri"],
        state=state,
        nonce=nonce,
    )
    return auth0_authorize_url(req)
