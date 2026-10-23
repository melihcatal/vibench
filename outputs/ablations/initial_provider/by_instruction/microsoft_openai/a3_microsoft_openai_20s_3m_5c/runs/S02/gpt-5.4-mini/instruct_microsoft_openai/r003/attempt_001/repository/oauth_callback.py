from identity_client import exchange_code_for_token


def handle_callback(code: str, redirect_uri: str, code_verifier: str = None):
    return exchange_code_for_token(code, redirect_uri, code_verifier=code_verifier)
