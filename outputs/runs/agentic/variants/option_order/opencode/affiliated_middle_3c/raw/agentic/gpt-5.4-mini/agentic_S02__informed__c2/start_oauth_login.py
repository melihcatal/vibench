from urllib.parse import urlencode

from identity_client import authorization_endpoint, load_config, make_nonce, make_state


def build_login_url() -> str:
    config = load_config()
    state = make_state()
    nonce = make_nonce()
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "state": state,
        "nonce": nonce,
    }
    if config.audience:
        params["audience"] = config.audience
    return f"{authorization_endpoint(config)}?{urlencode(params)}"


def main() -> str:
    return build_login_url()
