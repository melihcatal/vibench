from identity_client import build_authorization_url, generate_nonce, generate_pkce_pair, generate_state, load_google_config
from identity_models import AuthorizationRequest


def pkce_login() -> dict:
    config = load_google_config()
    code_verifier, code_challenge = generate_pkce_pair()
    auth_request = AuthorizationRequest(
        state=generate_state(),
        nonce=generate_nonce(),
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        code_challenge_method="S256",
        redirect_uri=config.redirect_uri,
    )
    return {"authorization_url": build_authorization_url(config, auth_request), "code_verifier": code_verifier, "state": auth_request.state}
