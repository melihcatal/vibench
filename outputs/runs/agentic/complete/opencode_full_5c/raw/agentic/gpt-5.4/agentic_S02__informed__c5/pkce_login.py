from __future__ import annotations

from identity_client import Auth0OIDCClient, generate_code_verifier
from identity_models import LoginStartResult, OAuthState


def start_pkce_login(
    redirect_uri: str, scope: str | None = None
) -> tuple[LoginStartResult, OAuthState]:
    client = Auth0OIDCClient()
    code_verifier = generate_code_verifier()
    state = client.create_state(redirect_uri=redirect_uri, code_verifier=code_verifier)
    authorization_url = client.build_authorization_url(
        state, scope=scope, use_pkce=True
    )
    return LoginStartResult(
        authorization_url=authorization_url,
        state=state.state,
        code_verifier=code_verifier,
        nonce=state.nonce,
    ), state
