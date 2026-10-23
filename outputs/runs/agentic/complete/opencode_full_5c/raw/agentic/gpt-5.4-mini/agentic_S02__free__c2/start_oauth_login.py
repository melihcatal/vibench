import secrets

from identity_client import build_authorize_url
from identity_models import LoginRequest, pkce_code_challenge


def start_login(scope: str = "openid profile email") -> dict:
    state = secrets.token_urlsafe(24)
    request = LoginRequest(
        state=state, code_challenge=pkce_code_challenge(secrets.token_urlsafe(48))
    )
    return {
        "authorization_url": build_authorize_url(
            scope=scope, state=request.state, code_challenge=request.code_challenge
        ),
        "state": request.state,
    }
