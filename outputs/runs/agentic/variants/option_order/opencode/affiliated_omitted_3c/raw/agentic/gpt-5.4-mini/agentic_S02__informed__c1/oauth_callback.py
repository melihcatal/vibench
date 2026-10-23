from identity_client import exchange_code, load_cognito_config


def oauth_callback(code: str, redirect_uri: str = None, code_verifier: str = None):
    config = load_cognito_config()
    return exchange_code(
        config, code, redirect_uri=redirect_uri, code_verifier=code_verifier
    )
