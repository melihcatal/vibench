from identity_client import exchange_code_for_tokens, load_identity_config
from identity_models import OAuthTokenResponse


def handle_callback(code: str, redirect_uri: str) -> OAuthTokenResponse:
    config = load_identity_config()
    payload = exchange_code_for_tokens(
        config["token_endpoint"],
        config["client_id"],
        config["client_secret"],
        code,
        redirect_uri,
    )
    return OAuthTokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type"),
        expires_in=payload.get("expires_in"),
    )
