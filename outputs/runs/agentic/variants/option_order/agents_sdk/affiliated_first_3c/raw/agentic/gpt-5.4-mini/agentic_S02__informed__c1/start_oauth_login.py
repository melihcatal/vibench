from __future__ import annotations

from identity_client import Auth0Client, build_auth0_client, generate_nonce, generate_state
from identity_models import OAuthAuthorizationRequest


def start_oauth_login(redirect_uri: str, scope: str = "openid profile email") -> str:
    client: Auth0Client = build_auth0_client()
    request = OAuthAuthorizationRequest(
        redirect_uri=redirect_uri,
        state=generate_state(),
        nonce=generate_nonce(),
        scope=scope,
        extra_params={"prompt": "login"},
    )
    return client.build_authorization_url(request)
