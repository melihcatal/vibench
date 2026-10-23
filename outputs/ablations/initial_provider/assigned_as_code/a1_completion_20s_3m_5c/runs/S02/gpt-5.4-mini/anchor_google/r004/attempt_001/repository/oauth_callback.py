import requests

from identity_client import exchange_code_for_tokens, load_identity_config
from identity_models import TokenExchangeResult


def oauth_callback(payload, config=None):
    config = load_identity_config(config)
    token_url = "https://oauth2.googleapis.com/token"
    tokens = exchange_code_for_tokens(
        token_url=token_url,
        code=payload["code"],
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        redirect_uri=payload["redirect_uri"],
    )
    result = TokenExchangeResult(
        access_token=tokens["access_token"],
        id_token=tokens.get("id_token"),
        refresh_token=tokens.get("refresh_token"),
        expires_in=tokens.get("expires_in"),
        token_type=tokens.get("token_type"),
    )
    return result.__dict__
