from identity_client import (
    load_identity_config,
    make_code_verifier,
    make_state,
    pkce_challenge,
)


def build_pkce_authorization_url(redirect_uri: str):
    config = load_identity_config()
    code_verifier = make_code_verifier()
    code_challenge = pkce_challenge(code_verifier)
    state = make_state()
    url = (
        f"{config['authorization_endpoint']}?response_type=code&client_id={config['client_id']}"
        f"&redirect_uri={redirect_uri}&scope=openid%20profile%20email&state={state}"
        f"&code_challenge={code_challenge}&code_challenge_method=S256"
    )
    return {"authorization_url": url, "code_verifier": code_verifier, "state": state}
