from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import OAuthCallbackRequest, TokenBundle


def handle_oauth_callback(request: OAuthCallbackRequest) -> TokenBundle:
    client = Auth0OIDCClient()
    token_response = client.exchange_code(
        code=request.code,
        redirect_uri=request.redirect_uri,
        code_verifier=request.code_verifier,
    )
    return TokenBundle(
        access_token=token_response["access_token"],
        id_token=token_response.get("id_token"),
        refresh_token=token_response.get("refresh_token"),
        token_type=token_response.get("token_type", "Bearer"),
        expires_in=token_response.get("expires_in"),
        scope=token_response.get("scope"),
        raw=token_response,
    )
