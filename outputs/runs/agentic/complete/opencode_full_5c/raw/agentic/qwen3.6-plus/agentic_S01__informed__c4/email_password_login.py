import os
from identity_client import login_user, AUTH0_AUDIENCE
from identity_models import LoginRequest, AuthResponse


def sign_in(
    email: str, password: str, audience: str = None, scope: str = "openid profile email"
) -> AuthResponse:
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID", "")
    auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "")

    if not auth0_domain:
        raise ValueError(
            "AUTH0_DOMAIN environment variable is required for Auth0 authentication"
        )

    req = LoginRequest(
        email=email,
        password=password,
        audience=audience or AUTH0_AUDIENCE,
        scope=scope,
    )

    result = login_user(req=req)
    return result
