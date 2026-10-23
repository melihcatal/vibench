from identity_client import exchange_code


def handle_callback(
    code: str, redirect_uri: str, code_verifier: str | None = None
) -> dict:
    return exchange_code(
        code=code, redirect_uri=redirect_uri, code_verifier=code_verifier
    )
