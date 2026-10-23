from __future__ import annotations

from urllib.parse import urlencode

from identity_client import build_oauth_config, generate_code_challenge, generate_code_verifier, generate_state
from identity_models import AuthorizationRequest


AUTH0_PKCE_METHOD = "S256"


def start_pkce_login() -> AuthorizationRequest:
    cfg = build_oauth_config()
    state = generate_state()
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    params = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": cfg.redirect_uri,
        "scope": " ".join(cfg.scopes),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": AUTH0_PKCE_METHOD,
    }
    if cfg.audience:
        params["audience"] = cfg.audience
    authorization_url = f"{cfg.authorization_endpoint}?{urlencode(params)}"
    return AuthorizationRequest(authorization_url=authorization_url, state=state, code_verifier=code_verifier)
