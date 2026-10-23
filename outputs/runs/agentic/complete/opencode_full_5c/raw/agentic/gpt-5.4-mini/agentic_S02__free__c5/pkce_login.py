from identity_client import AUTH0_REDIRECT_URI, auth0_authorize_url, pkce_pair
from identity_models import LoginRequest


def start_pkce_login() -> dict:
    pair = pkce_pair()
    request = LoginRequest(
        client_id="auth0",
        redirect_uri=AUTH0_REDIRECT_URI,
        state="pkce-state",
        nonce="pkce-nonce",
    )
    return {
        "authorization_url": auth0_authorize_url(
            request.state, request.nonce, pair["code_challenge"]
        ),
        "code_verifier": pair["code_verifier"],
    }
