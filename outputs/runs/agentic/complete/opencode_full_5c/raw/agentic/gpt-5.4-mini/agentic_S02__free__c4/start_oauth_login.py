import os
import secrets
from urllib.parse import urlencode
from identity_client import get_oidc_config, build_redirect_uri


def start_oauth_login(state=None, nonce=None, scope=None):
    cfg = get_oidc_config()
    state = state or secrets.token_urlsafe(24)
    nonce = nonce or secrets.token_urlsafe(24)
    scope = scope or cfg["scope"]
    params = {
        "client_id": cfg["client_id"],
        "response_type": "code",
        "redirect_uri": build_redirect_uri(cfg),
        "scope": scope,
        "state": state,
        "nonce": nonce,
    }
    if cfg.get("code_challenge"):
        params["code_challenge"] = cfg["code_challenge"]
        params["code_challenge_method"] = cfg.get("code_challenge_method", "S256")
    return {"authorization_url": f"{cfg['authorization_endpoint']}?{urlencode(params)}", "state": state, "nonce": nonce}
