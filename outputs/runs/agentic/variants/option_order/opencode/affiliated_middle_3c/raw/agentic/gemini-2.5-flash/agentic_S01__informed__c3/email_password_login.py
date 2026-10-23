import os
from auth0.management import Auth0
from auth0.authentication import Auth0Authentication
from identity_models import LoginRequest, LoginResponse


def email_password_login(request: LoginRequest) -> LoginResponse:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    auth0 = Auth0Authentication(domain, client_id)

    token_response = auth0.login(
        username=request.email,
        password=request.password,
        scope="openid profile email",
        audience=os.environ.get("AUTH0_AUDIENCE"),
    )

    return LoginResponse(
        access_token=token_response["access_token"],
        id_token=token_response["id_token"],
        refresh_token=token_response.get("refresh_token"),
        expires_in=token_response["expires_in"],
    )
