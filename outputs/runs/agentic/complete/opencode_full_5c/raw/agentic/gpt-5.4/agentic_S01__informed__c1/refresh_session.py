from __future__ import annotations

from identity_client import Auth0Client
from identity_models import RefreshSessionRequest, TokenSet


def refresh_session(
    refresh_token: str, scope: str = "openid profile email offline_access"
) -> TokenSet:
    request = RefreshSessionRequest(refresh_token=refresh_token, scope=scope)
    client = Auth0Client()
    token_data = client.refresh_token(request.refresh_token, request.scope)
    return TokenSet.from_auth0_token_response(token_data)
