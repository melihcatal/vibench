from identity_client import AUTH0_REDIRECT_URI, auth0_authorize_url
from identity_models import LoginRequest


def build_start_login(request: LoginRequest) -> str:
    return auth0_authorize_url(request.state, request.nonce)


def start_oauth_login() -> str:
    request = LoginRequest(
        client_id="auth0",
        redirect_uri=AUTH0_REDIRECT_URI,
        state="login-state",
        nonce="login-nonce",
    )
    return build_start_login(request)
