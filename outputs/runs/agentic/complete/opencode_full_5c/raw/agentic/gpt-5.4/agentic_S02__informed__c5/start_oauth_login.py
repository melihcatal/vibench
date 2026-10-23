from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import LoginStartResult, OAuthState


def start_oauth_login(
    redirect_uri: str, scope: str | None = None
) -> tuple[LoginStartResult, OAuthState]:
    client = Auth0OIDCClient()
    state = client.create_state(redirect_uri=redirect_uri)
    authorization_url = client.build_authorization_url(
        state, scope=scope, use_pkce=False
    )
    return LoginStartResult(
        authorization_url=authorization_url,
        state=state.state,
        nonce=state.nonce,
    ), state
