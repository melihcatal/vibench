import secrets
from urllib.parse import urlencode

from identity_client import authorize_endpoint, load_oauth_config


def build_login_url(state: str | None = None, nonce: str | None = None, code_challenge: str | None = None) -> str:
    config = load_oauth_config()
    state = state or secrets.token_urlsafe(24)
    nonce = nonce or secrets.token_urlsafe(24)
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "redirect_uri": config.redirect_uri,
        "response_mode": "query",
        "scope": " ".join(config.scopes),
        "state": state,
        "nonce": nonce,
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return f"{authorize_endpoint(config)}?{urlencode(params)}"
