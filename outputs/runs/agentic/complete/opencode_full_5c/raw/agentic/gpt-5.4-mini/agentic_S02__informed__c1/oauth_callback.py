from identity_client import exchange_code_for_tokens, load_config
from identity_models import OAuthTokenResponse


def oauth_callback(code: str, code_verifier: str = "") -> OAuthTokenResponse:
    config = load_config()
    tokens = exchange_code_for_tokens(config, code, code_verifier or None)
    return OAuthTokenResponse(
        access_token=tokens.get("access_token", ""),
        id_token=tokens.get("id_token", ""),
        refresh_token=tokens.get("refresh_token", ""),
        token_type=tokens.get("token_type", "Bearer"),
        expires_in=int(tokens.get("expires_in", 0)),
        raw=tokens,
    )
