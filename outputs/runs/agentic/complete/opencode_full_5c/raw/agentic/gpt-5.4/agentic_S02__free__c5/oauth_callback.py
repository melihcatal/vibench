from __future__ import annotations

from identity_client import exchange_code_for_tokens
from identity_models import TokenExchangeRequest, to_dict


def oauth_callback(request: TokenExchangeRequest) -> dict:
    tokens = exchange_code_for_tokens(
        code=request.code,
        redirect_uri=request.redirect_uri,
        code_verifier=request.code_verifier,
    )
    response = to_dict(tokens)
    response["provider"] = "auth0"
    response["token_endpoint"] = (
        "https://" + __import__("os").environ["AUTH0_DOMAIN"] + "/oauth/token"
    )
    return response
