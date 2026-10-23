from urllib.parse import urlencode

from identity_client import (
    authorization_endpoint,
    load_config,
    make_nonce,
    make_pkce_challenge,
    make_pkce_verifier,
    make_state,
)


def build_pkce_login_url():
    config = load_config()
    verifier = make_pkce_verifier()
    challenge = make_pkce_challenge(verifier)
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "state": make_state(),
        "nonce": make_nonce(),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if config.audience:
        params["audience"] = config.audience
    return f"{authorization_endpoint(config)}?{urlencode(params)}", verifier
