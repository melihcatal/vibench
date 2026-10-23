from identity_client import exchange_code_for_tokens, load_identity_config
from identity_models import OAuthTokenSet


def oauth_callback(payload, config=None):
    config = config or load_identity_config()
    tokens = exchange_code_for_tokens(
        payload["code"],
        payload["redirect_uri"],
        config,
        payload.get("code_verifier"),
    )
    token_set = OAuthTokenSet(
        access_token=tokens["access_token"],
        id_token=tokens.get("id_token"),
        refresh_token=tokens.get("refresh_token"),
        token_type=tokens.get("token_type"),
        expires_in=tokens.get("expires_in"),
    )
    return {"tokens": token_set.__dict__}
