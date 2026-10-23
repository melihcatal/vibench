from __future__ import annotations

from urllib.parse import urlencode

from identity_client import build_oauth_config, generate_state
from identity_models import AuthorizationRequest


def start_oauth_login() -> AuthorizationRequest:
    cfg = build_oauth_config()
    state = generate_state()
    params = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": cfg.redirect_uri,
        "scope": " ".join(cfg.scopes),
        "state": state,
    }
    if cfg.audience:
        params["audience"] = cfg.audience
    authorization_url = f"{cfg.authorization_endpoint}?{urlencode(params)}"
    return AuthorizationRequest(authorization_url=authorization_url, state=state)
