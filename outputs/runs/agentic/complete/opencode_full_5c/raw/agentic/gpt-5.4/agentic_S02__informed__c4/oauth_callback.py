from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import OAuthCallbackRequest, TokenSet


def handle_oauth_callback(request: OAuthCallbackRequest) -> TokenSet:
    client = Auth0OIDCClient()
    token_payload = client.exchange_code(
        code=request.code,
        redirect_uri=request.redirect_uri,
        code_verifier=request.code_verifier,
    )
    return TokenSet.from_dict(token_payload)
