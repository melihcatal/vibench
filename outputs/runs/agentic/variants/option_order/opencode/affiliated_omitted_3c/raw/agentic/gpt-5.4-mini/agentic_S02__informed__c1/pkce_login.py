from identity_client import (
    build_authorize_url,
    load_cognito_config,
    new_nonce,
    new_state,
    pkce_pair,
)


def pkce_login():
    config = load_cognito_config()
    pair = pkce_pair()
    return {
        "authorization_url": build_authorize_url(
            config,
            state=new_state(),
            nonce=new_nonce(),
            code_challenge=pair["code_challenge"],
        ),
        "code_verifier": pair["code_verifier"],
    }
