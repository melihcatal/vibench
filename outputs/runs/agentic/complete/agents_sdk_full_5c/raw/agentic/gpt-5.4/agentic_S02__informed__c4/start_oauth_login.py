from __future__ import annotations

from identity_client import build_auth0_authorization_url, generate_state, load_auth0_config
from identity_models import OAuthStartRequest



def start_oauth_login(request: OAuthStartRequest) -> dict:
    config = load_auth0_config()
    redirect_uri = request.redirect_uri or config.default_redirect_uri
    if not redirect_uri:
        raise ValueError("redirect_uri is required for Auth0 authorization")
    scope = " ".join(request.scope)
    authorization_url = build_auth0_authorization_url(
        redirect_uri=redirect_uri,
        state=request.state or generate_state(),
        scope=scope,
        audience=request.audience,
        prompt=request.prompt,
    )
    return {
        "provider": "Auth0 Authentication API",
        "issuer": config.issuer,
        "authorization_url": authorization_url,
        "redirect_uri": redirect_uri,
    }
