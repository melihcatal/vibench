from __future__ import annotations

from identity_client import exchange_code_for_tokens
from identity_models import OAuthCallbackRequest


def oauth_callback(request: OAuthCallbackRequest) -> dict:
    tokens = exchange_code_for_tokens(
        code=request.code,
        redirect_uri=request.redirect_uri,
        code_verifier=request.code_verifier,
    )
    result = tokens.to_dict()
    if request.state:
        result["state"] = request.state
    return result
