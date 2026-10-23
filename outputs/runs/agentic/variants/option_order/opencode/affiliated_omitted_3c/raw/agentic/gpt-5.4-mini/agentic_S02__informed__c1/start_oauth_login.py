from identity_client import (
    build_authorize_url,
    load_cognito_config,
    new_nonce,
    new_state,
)


def start_oauth_login() -> str:
    config = load_cognito_config()
    return build_authorize_url(config, state=new_state(), nonce=new_nonce())
