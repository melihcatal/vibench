from identity_client import exchange_code_for_tokens, load_identity_config


def handle_oauth_callback(code: str, redirect_uri: str, code_verifier: str = ""):
    config = load_identity_config()
    return exchange_code_for_tokens(config, code, redirect_uri, code_verifier)
