from __future__ import annotations

import os
from urllib.parse import urlencode

from identity_client import get_identity_settings
from identity_models import LoginRequest


AUTH0_AUTHORIZE_HOST = "https://{domain}/authorize"


def build_authorization_url(request: LoginRequest) -> str:
    settings = get_identity_settings()
    base_url = AUTH0_AUTHORIZE_HOST.format(domain=settings.auth0_domain)
    params = {
        "client_id": settings.client_id,
        "response_type": "code",
        "redirect_uri": request.redirect_uri or settings.redirect_uri,
        "scope": request.scope or settings.scopes,
        "state": request.state,
        "audience": settings.audience,
    }
    if request.nonce:
        params["nonce"] = request.nonce
    if request.prompt:
        params["prompt"] = request.prompt
    if request.connection:
        params["connection"] = request.connection
    return f"{base_url}?{urlencode(params)}"


def start_oauth_login(request: LoginRequest) -> str:
    return build_authorization_url(request)


if __name__ == "__main__":
    state = os.getenv("OIDC_STATE", "example-state")
    redirect_uri = os.getenv("OIDC_REDIRECT_URI")
    scope = os.getenv("OIDC_SCOPE", "openid profile email")
    print(start_oauth_login(LoginRequest(state=state, redirect_uri=redirect_uri, scope=scope)))
