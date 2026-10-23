from identity_client import (
    auth0_authorize_url,
    generate_nonce,
    generate_state,
    load_config,
)
from identity_models import OAuthLoginRequest


def start_oauth_login() -> dict:
    config = load_config()
    request = OAuthLoginRequest(
        redirect_uri=config.redirect_uri, state=generate_state(), nonce=generate_nonce()
    )
    return {
        "authorization_url": auth0_authorize_url(
            config, request.state, request.nonce, request.scope
        ),
        "state": request.state,
        "nonce": request.nonce,
    }
