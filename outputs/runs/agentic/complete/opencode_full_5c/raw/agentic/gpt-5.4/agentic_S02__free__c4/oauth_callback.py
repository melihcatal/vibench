from __future__ import annotations

from identity_client import exchange_code_for_tokens, load_okta_config
from identity_models import CallbackRequest, TokenSet


def oauth_callback(callback: CallbackRequest) -> dict:
    config = load_okta_config()
    token_payload = exchange_code_for_tokens(
        code=callback.code,
        redirect_uri=callback.redirect_uri,
        code_verifier=callback.code_verifier,
    )
    token_set = TokenSet.from_dict(token_payload)
    return {
        "provider": "okta",
        "issuer": config.issuer,
        "tokens": token_set.to_dict(),
        "state": callback.state,
    }
