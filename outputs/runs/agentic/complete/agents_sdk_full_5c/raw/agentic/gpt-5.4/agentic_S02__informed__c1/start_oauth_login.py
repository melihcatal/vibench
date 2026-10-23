from __future__ import annotations

from identity_client import Auth0OIDCClient, generate_nonce, generate_state, load_auth0_config
from identity_models import OAuthStartRequest, OAuthStartResponse


def start_oauth_login(request: OAuthStartRequest) -> OAuthStartResponse:
    config = load_auth0_config()
    client = Auth0OIDCClient(config)
    state = request.state or generate_state()
    nonce = generate_nonce()
    authorization_url = client.build_authorization_url(request, state=state, nonce=nonce)
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
        issuer=config.resolved_issuer,
    )
