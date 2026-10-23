from identity_client import exchange_code_for_tokens, get_google_client_config
from identity_models import OAuthTokenResponse


def oauth_callback(code: str, code_verifier: str = "") -> OAuthTokenResponse:
    config = get_google_client_config()
    payload = exchange_code_for_tokens(code, config["redirect_uri"], config["client_id"], config["client_secret"], code_verifier or None)
    return OAuthTokenResponse(
        access_token=payload.get("access_token", ""),
        id_token=payload.get("id_token", ""),
        refresh_token=payload.get("refresh_token", ""),
        token_type=payload.get("token_type", "Bearer"),
        expires_in=int(payload.get("expires_in", 0)),
    )
