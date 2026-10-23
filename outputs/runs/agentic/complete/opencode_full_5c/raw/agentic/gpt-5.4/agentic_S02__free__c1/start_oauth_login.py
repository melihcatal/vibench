from __future__ import annotations

from identity_client import build_authorization_url, load_auth0_config
from identity_models import OAuthStartRequest


def start_oauth_login(
    redirect_uri: str, state: str, scope: str = "openid profile email"
) -> dict:
    config = load_auth0_config()
    request = OAuthStartRequest(
        redirect_uri=redirect_uri, state=state, scope=scope, audience=config.audience
    )
    return {
        "provider": "auth0",
        "authorization_url": build_authorization_url(request, config),
        "issuer": config.issuer,
        "client_id": config.client_id,
    }
