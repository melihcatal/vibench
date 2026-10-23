from identity_client import exchange_code_for_tokens, get_cognito_config


def oauth_callback(code: str, state: str | None = None, code_verifier: str | None = None) -> dict:
    cfg = get_cognito_config()
    tokens = exchange_code_for_tokens(code, cfg["redirect_uri"], code_verifier)
    return {"state": state, "tokens": tokens}
