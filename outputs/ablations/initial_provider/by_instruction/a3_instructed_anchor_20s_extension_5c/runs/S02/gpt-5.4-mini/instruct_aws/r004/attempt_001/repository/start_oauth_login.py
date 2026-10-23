import urllib.parse

from identity_client import load_identity_config


def start_oauth_login(state: str, nonce: str | None = None) -> str:
    cfg = load_identity_config()
    params = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": cfg.redirect_uri,
        "scope": cfg.scope,
        "state": state,
    }
    if nonce:
        params["nonce"] = nonce
    return f"{cfg.authorize_url}?{urllib.parse.urlencode(params)}"
