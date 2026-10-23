from identity_client import exchange_code_for_tokens, load_google_config


def oauth_callback(code: str, redirect_uri: str | None = None, code_verifier: str | None = None):
    config = load_google_config()
    return exchange_code_for_tokens(config, code, redirect_uri=redirect_uri, code_verifier=code_verifier)
