from identity_client import exchange_code_for_tokens


def oauth_callback(
    code: str, redirect_uri: str, code_verifier: str | None = None
) -> dict:
    tokens = exchange_code_for_tokens(
        code=code, redirect_uri=redirect_uri, code_verifier=code_verifier
    )
    return tokens.__dict__
