from identity_client import (
    auth0_authorize_url,
    generate_code_verifier,
    generate_nonce,
    generate_state,
    load_config,
    pkce_challenge,
)
from identity_models import OAuthLoginRequest


def pkce_login() -> dict:
    config = load_config()
    code_verifier = generate_code_verifier()
    request = OAuthLoginRequest(
        redirect_uri=config.redirect_uri,
        state=generate_state(),
        nonce=generate_nonce(),
        code_verifier=code_verifier,
        code_challenge=pkce_challenge(code_verifier),
    )
    url = auth0_authorize_url(config, request.state, request.nonce, request.scope)
    return {
        "authorization_url": f"{url}&code_challenge={request.code_challenge}&code_challenge_method={request.code_challenge_method}",
        "code_verifier": request.code_verifier,
        "state": request.state,
    }
