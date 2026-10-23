from identity_client import build_authorization_url, create_code_challenge, create_code_verifier, create_nonce, create_state, get_google_client_config


def pkce_login() -> dict[str, str]:
    config = get_google_client_config()
    state = create_state()
    nonce = create_nonce()
    verifier = create_code_verifier()
    challenge = create_code_challenge(verifier)
    url = build_authorization_url(config["client_id"], config["redirect_uri"], state, nonce, ["openid", "email", "profile"], challenge)
    return {"authorization_url": url, "state": state, "nonce": nonce, "code_verifier": verifier}
