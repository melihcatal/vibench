from __future__ import annotations

from identity_client import (
    AUTH0_AUTHORIZATION_ENDPOINT,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
    AUTH0_ISSUER,
    build_authorization_url,
    new_nonce,
    new_state,
)
from identity_models import AuthorizationRequest


def start_oauth_login(scope: str = "openid profile email") -> dict[str, str]:
    state = new_state()
    nonce = new_nonce()
    request_obj = AuthorizationRequest(
        authorization_endpoint=AUTH0_AUTHORIZATION_ENDPOINT,
        client_id=AUTH0_CLIENT_ID,
        redirect_uri=AUTH0_REDIRECT_URI,
        scope=scope,
        state=state,
        nonce=nonce,
    )
    return {
        "issuer": AUTH0_ISSUER,
        "authorization_url": build_authorization_url(request_obj),
        "state": state,
        "nonce": nonce,
    }
