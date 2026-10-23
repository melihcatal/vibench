import secrets
from urllib.parse import urlencode

from identity_client import load_config


def start_oauth_login(redirect_uri: str) -> str:
    config = load_config()
    state = secrets.token_urlsafe(24)
    nonce = secrets.token_urlsafe(24)
    params = {
        "client_id": config.auth0_client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
    }
    if config.auth0_audience:
        params["audience"] = config.auth0_audience
    return f"https://{config.auth0_domain}/authorize?{urlencode(params)}"
