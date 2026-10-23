import os
import secrets
from urllib.parse import urlencode

from identity_client import build_oidc_authorize_url, get_identity_config
from identity_models import LoginStartRequest, LoginStartResponse


def start_oauth_login(request: LoginStartRequest | None = None) -> LoginStartResponse:
    config = get_identity_config()
    state = request.state if request and request.state else secrets.token_urlsafe(24)
    nonce = request.nonce if request and request.nonce else secrets.token_urlsafe(24)
    authorize_url = build_oidc_authorize_url(
        config=config,
        state=state,
        nonce=nonce,
        prompt=request.prompt if request else None,
        login_hint=request.login_hint if request else None,
        scope=request.scope if request else None,
    )
    return LoginStartResponse(authorize_url=authorize_url, state=state, nonce=nonce, provider="Auth0")


if __name__ == "__main__":
    print(start_oauth_login())
