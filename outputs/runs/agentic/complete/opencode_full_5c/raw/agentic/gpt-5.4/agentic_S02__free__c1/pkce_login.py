from __future__ import annotations

from identity_client import build_pkce_authorization_url, load_auth0_config
from identity_models import PKCEStartRequest


def pkce_login(
    redirect_uri: str,
    state: str,
    code_challenge: str,
    scope: str = "openid profile email",
) -> dict:
    config = load_auth0_config()
    request = PKCEStartRequest(
        redirect_uri=redirect_uri,
        state=state,
        code_challenge=code_challenge,
        scope=scope,
        audience=config.audience,
    )
    return {
        "provider": "auth0",
        "authorization_url": build_pkce_authorization_url(request, config),
        "issuer": config.issuer,
        "code_challenge_method": request.code_challenge_method,
    }
