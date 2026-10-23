from identity_client import exchange_code_for_tokens, load_identity_config
from identity_models import TokenResponse


def oauth_callback(payload, config=None):
    config = load_identity_config(config)
    tokens = exchange_code_for_tokens(config, payload["code"], payload["redirect_uri"])
    return TokenResponse(access_token=tokens["access_token"], id_token=tokens.get("id_token"), refresh_token=tokens.get("refresh_token"), token_type=tokens.get("token_type"), expires_in=tokens.get("expires_in")).__dict__
